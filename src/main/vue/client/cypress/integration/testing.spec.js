/*
const Chance = require('chance')
const chance = new Chance();

// URL des testservers
const url = 'https://localhost:8080';

context('GUI Test', () => {
    beforeEach(() => {
        // URL wird besucht
        cy.visit(url)
    })

    it('tests if localhosts redirects', () => {
        cy.url().should('include', 'login');
        cy.get('input[name=username]').type(chance.email());
        cy.get('input[name=password]').type(chance.string());
    })
});

context('REST Test', () => {
    /!*
    Ein bestimmter Test
     *!/
    it('tests project creation', ()=>{
        cy.request('POST', url+'/functions/project/ping').then((response) => {
            //expect(response.body).to.have.property('name', 'Jane')
            expect(response.body).to.eq('pong') // true
        })

    })
})
*/
