const fastify = require('fastify')();
const path = require('path');
const argon2 = require('argon2');

const { User, Note } = require('./models');

// object from report.js
const report = require('./report');

fastify.register(require('fastify-formbody'));

fastify.register(require('fastify-secure-session'), { 
	key: require('crypto').randomBytes(32)
});

fastify.register(require('fastify-csrf'), {
	sessionPlugin: 'fastify-secure-session'
});

fastify.register(require('point-of-view'), {
	engine: {
		ejs: require('ejs')
	},
	// this is like open_basedir for PHP, setting root directory
	root: path.join(__dirname, 'views')
});

// executed before a route is called, getting notes data from username which is parsed from the session
// like @auth_required from FLASK decorator for routes.
fastify.addHook('preHandler', async (req, res) => {
	if (req.session.get('user')) {
		req.user = await User.findOne({ where: { username: req.session.get('user') }, include: ['notes'] });
	}
});

// if there's no user in the session then redirect to '/'
function auth(handler) {
	return (req, res) => {
		if (!req.user) return res.redirect('/');

		return handler(req, res);
	}
}


// lenght constraints on username + password
let userSchema = {
	body: {
		type: 'object',
		properties: {
			username: { type: 'string', maxLength: 30 },
			password: { type: 'string', maxLength: 30 }
		},
		required: ['username', 'password']
	}
};


// the max lenght of the URL is 1000, interesting...
let reportSchema = {
	body: {
		type: 'object',
		properties: {
			url: { type: 'string', maxLength: 1000 },
		},
		required: ['url']
	}
}

// also interesting how the body of the note has a 1,000 character limit.
let noteSchema = {
	body: {
		type: 'object',
		properties: {
			title: { type: 'string', maxLength: 30 },
			content: { type: 'string', maxLength: 1000 }
		},
		required: ['title', 'content']
	}
};

// an ID is needed to delete a note.
let deleteSchema = {
	body: {
		type: 'object',
		properties: {
			id: { type: 'integer' }
		},
		required: ['id']
	}
}

fastify.after(() => {
	fastify.get('/', (req, res) => {
		// if there is a user redirect to /notes
		if (req.user) return res.redirect('/notes');
		// otherwise login
		return res.view('login');
	});

	fastify.post('/login', { schema: userSchema }, async (req, res) => {
		let { username, password } = req.body;
		username = username.toLowerCase();

		let user = await User.findOne({ where: { username }});
		
		// if user isn't found say not found
		if (user === null) {
			return res.status(400).send('User not found');
		}

		// if you have the right username but the wrong password let the user know
		if (!(await argon2.verify(user.password, password))) {
			return res.status(400).send('Wrong password!');
		}

		// set the session to the username
		req.session.set('user', user.username);

		return res.redirect('/notes');
	});

	fastify.get('/register', (req, res) => {
		return res.view('register');
	});

	fastify.post('/register', { schema: userSchema }, async (req, res) => {
		/* NOTE: interesting how there's no CSRF on this endpoint */
		// parsing username and password from our body
		let { username, password } = req.body;
		username = username.toLowerCase();

		// finding an instance of that username, if it exists throw 400
		let user = await User.findOne({ where: { username }});
		if (user) {
			return res.status(400).send('User already exists!');
		}

		// create that user object using argon2 hash (secure)
		await User.create({
			username,
			password: await argon2.hash(password)
		});

		// like flask the session is set to a username not a UUID (maybe we can login as any user and retrieve note with flag?)
		req.session.set('user', username);

		return res.redirect('/notes');
	});

	fastify.get('/notes', auth(async (req, res) => {
		// interesting how there's a CSRF being generated here.
		return res.view('notes', {
			notes: req.user.notes, 
			csrf: await res.generateCsrf()
		});
	}));

	fastify.get('/new', auth(async (req, res) => {
		return res.view('new', { csrf: await res.generateCsrf() });	
	}));

	fastify.post('/new', {
		schema: noteSchema,
		preHandler: fastify.csrfProtection
	}, auth(async (req, res) => {
		// getting title and content from POST body
		let { title, content } = req.body;

		// our note is stored in correspondence to userID pulled from our session (again, maybe session vuln?)
		await Note.create({
			title,
			content,
			userId: req.user.id
		});

		return res.redirect('/notes');
	}));

	fastify.post('/delete', {
		schema: deleteSchema,
		preHandler: fastify.csrfProtection
	}, auth(async (req, res) => {
		
		let { id } = req.body;

		let deleted = false;

		for (let note of req.user.notes) {
			if (note.id === id) {
				await note.destroy();

				deleted = true;
			}
		}

		if (deleted) {
			return res.redirect('/notes');
		} else {
			res.status(400).send('Note not found!');
		}
	}));

	fastify.get('/report', auth(async (req, res) => {
		return res.view('report', { csrf: await res.generateCsrf() });
	}));

	fastify.post('/report', {
		schema: reportSchema,
		preHandler: fastify.csrfProtection
	}, auth((req, res) => {
		let { url } = req.body;

		if (report.open) {
			return res.send('Only one browser can be open at a time!');
		} else {
			report.run(url);
		}

		return res.send('URL has been reported.');
	}));
}) 

fastify.listen(8080, '0.0.0.0');