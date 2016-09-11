#!/usr/bin/env node

var readline = require('readline');
var Bluebird = require('bluebird');

var login = require('./tucan-login');
var fs = require('fs');

var BASE_URL = 'https://www.tucan.tu-darmstadt.de';

var SCREENSHOT_FILENAME = 'grades.png';
var GRADES_JSON_FILENAME = 'grades.json';

var SELECTORS = {
    Prüfungen: 'li[title="Prüfungen"] a.depth_1',
    Leistungsspiegel: 'li[title="Leistungsspiegel"] a.depth_2'
};

var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

askQuestion('TuCan User: ')
    .then(function(user) {
        return [user, askQuestion('TuCan Password (it\'s safe with me, yes, yes) ')];
    })
    .all()
    .spread(getGrades)
    .catch(function(err) {
        console.error(err);
        process.exit(1);
    });

function getGrades(user, password) {
    return login
        .login(user, password, BASE_URL)
        .waitForSelector(SELECTORS.Prüfungen)
        .click(SELECTORS.Prüfungen)
        .waitForSelector(SELECTORS.Leistungsspiegel)
        .waitForNextPage()
        .click(SELECTORS.Leistungsspiegel)
        .waitForSelector(SELECTORS.Leistungsspiegel)
        .waitForNextPage()
        .evaluate(function(done) {
            var result = jQuery('.students_results tr img[src$=\"pass.gif\"]')
                .map(function(index, item) {
                    var $item = jQuery(item);
                    var $parent = $item.closest('tr');

                    function getChild(num, a) {
                        return $parent.find('td:nth-child(%NUM%)'.replace('%NUM%', num) + (a ? ' a' : '')).text().trim();
                    }

                    return {
                        nr: getChild(1),
                        name: getChild(2, true),
                        cp: getChild(4),
                        grade: getChild(6)
                    };
                })
                .filter(function(index, item) {
                    return !!item.grade;
                })
                .toArray();
            done(null, result);
        })
        .then(function(grades) {
            fs.writeFileSync(GRADES_JSON_FILENAME, JSON.stringify(grades, null, '\t'), {
                encoding: 'utf-8'
            });
        })
        .screenshot(SCREENSHOT_FILENAME)
        .close()
        .tap(function() {
            console.info('Finished! See ' + GRADES_JSON_FILENAME + ' and ' + SCREENSHOT_FILENAME);
            process.exit(0);
        });
}

function askQuestion(question) {
    return new Bluebird(function(resolve) {
        rl.question(question, function(result) {
            resolve(result);
        });
    });
}
