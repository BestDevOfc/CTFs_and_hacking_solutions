const some_list = ['value', '2wfTpTR', 'instantiate', '275341bEPcme', 'innerHTML', '1195047NznhZg', '1qfevql', 'input', '1699808QuoWhA', 'Correct!', 'check_flag', 'Incorrect!', './JIFxzHyW8W', '23SMpAuA', '802698XOMSrr', 'charCodeAt', '474547vVoGDO', 'getElementById', 'instance', 'copy_char', '43591XxcWUl', '504454llVtzW', 'arrayBuffer', '2NIQmVj', 'result'];

const function_one = function(parameter_one, _0x53c021) {
    parameter_one = parameter_one - 470;
    let something_from_list = some_list[parameter_one];
    return something_from_list;
};
(function(parameter_one) {
    while (!![]) {
        try {
            const negative_sum = -parseInt(function_one(491)) + parseInt(function_one(493)) + -parseInt(function_one(475)) * -parseInt(function_one(473)) + -parseInt(function_one(482)) * -parseInt(function_one(483)) + -parseInt(function_one(478)) * parseInt(function_one(480)) + parseInt(function_one(472)) * parseInt(function_one(490)) + -parseInt(function_one(485));
            if (negative_sum === 627907) break;
            else parameter_one['push'](parameter_one['shift']());
        } catch (_0x41d31a) { //  4313882?
            parameter_one['push'](parameter_one['shift']());
        }
    }
}(some_list));

let exports; // this stores the functions, objects, etc of the WASM binary that can now be used directly in JS
(async () => {
    let wasm_binary = await fetch("./JIFxzHyW8W"), // fetching the Web assembly binary from the website
        wasm_binary_to_array_bytes = await WebAssembly['instantiate'](await wasm_binary['arrayBuffer']()),
        wasm_instance = wasm_binary_to_array_bytes['instance'];
    exports = wasm_instance['exports'];
})();

function onButtonPress() {
    let user_input = document['getElementById'](function_one(484))[function_one(477)];
    for (let i = 0; i < user_input['length']; i++) {
        exports['copy_char']( user_input['charCodeAt'](i), i );
        // exports['copy_char']( ASCII_representation_of(index),  );
    }
    
    exports['copy_char'](0, user_input['length']);
    exports['check_flag']() == 1 ? 'Correct!' : 'Incorrect!';
}