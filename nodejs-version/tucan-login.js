/* jshint node: true */
var horseman = new require('node-horseman')();

var SELECTORS = {
    LoginUser: '#field_user',
    LoginPass: '#field_pass',
    LoginSubmit: '#logIn_btn',
    Veranstaltungen: 'li[title="Veranstaltungen"] a'
};

module.exports.login = function login(username, password, baseUrl) {
    console.log('Logging in:', username, 'password:', password);
    var selectors = SELECTORS;
    return horseman
        .open(baseUrl)
        .waitForSelector(selectors.LoginSubmit)
        .type(selectors.LoginUser, username)
        .type(selectors.LoginPass, password)
        .click(selectors.LoginSubmit)
        .waitForSelector(selectors.Veranstaltungen);
};
