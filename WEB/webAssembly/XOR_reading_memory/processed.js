const some_list = ['copy_char', 'value', '207aLjBod', '1301420SaUSqf', '233ZRpipt', '2224QffgXU', 'check_flag', '408533hsoVYx', 'instance', '278338GVFUrH', 'Correct!', '549933ZVjkwI', 'innerHTML', 'charCodeAt', './aD8SvhyVkb', 'result', '977AzKzwq', 'Incorrect!', 'exports', 'length', 'getElementById', '1jIrMBu', 'input', '615361geljRK'];
const function_one = function(parameter_one, _0x4d6e6c) {
    parameter_one = parameter_one - 195;
    let list_element = some_list[parameter_one];
    return list_element;
};
(function(some_list) {
    while (!![]) {
        try {
            const result = -parseInt(function_one(0xc8)) * -parseInt(function_one(0xc9)) + -parseInt(function_one(0xcd)) + parseInt(function_one(0xcf)) + parseInt(function_one(0xc3)) + -parseInt(function_one(0xc6)) * parseInt(function_one(0xd4)) + parseInt(function_one(0xcb)) + -parseInt(function_one(0xd9)) * parseInt(function_one(0xc7));
            if (result === 310022) break;
            else some_list['push'](some_list['shift']());
        } catch (_0x4f8a) { // what is this catch for, errors???
            some_list['push'](some_list['shift']());
        }
    }
}(some_list));
let exports;
(async () => {
    let wasm_binary = await fetch('./aD8SvhyVkb'),
        wasm_array = await WebAssembly['instantiate'](await wasm_binary['arrayBuffer']()),
        wasm_object = wasm_array[function_one(0xcc)];
    exports = wasm_object['exports'];
})();

function onButtonPress() {
    let user_input = document[function_one(0xd8)](function_one(0xda))[function_one(0xc5)];
    
    for (let i = 0; i < user_input['length']; i++) {
        exports['copy_char'](user_input['charCodeAt'](i), i);
    }
    
    exports['copy_char'](0, user_input['length']);
    
    if( exports['check_flag']() == 1 ){
        "correct";
    }
    else
    {
        "incorrect";
    }
}










