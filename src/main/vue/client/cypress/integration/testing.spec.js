const Chance = require('chance')
const chance = new Chance();

const url = 'http://localhost:8080/#/';

context('GUI Test', () => {
    beforeEach(() => {
        cy.visit(url)
    })

    it('Test create student', () => {

        var length_before = cy.get('#tbody').find('tr');
        var email = chance.email()
        cy.get('#addStudentEmail').type(email);
        cy.get('#addStudentUsername').type(chance.string());
        cy.get('#createStudentButton').click();

        cy.get('#tbody').contains(email)
    })
});
