const faker = require('faker');

context('User Actions', ()=>{
    let email
    let username
    let password
    before(()=> {
        email = faker.internet.email()
        username = faker.internet.userName()
        password = faker.internet.password()
        cy.register(email, username, password)
    })
    beforeEach(() =>{
        //sign in
        cy.login(username, password)
    })

    it('should not show any projects after the first time sign in', ()=> {
        //assert is fresh user and is on homepage
        cy.get('a.btn-primary').contains('Create New Project')
        cy.get('div#project-background > h3').contains('No Projects')
    })
    it('should show info on user profile correctly', () =>{
        cy.get("a#profile").click()

        cy.get('span#username').contains(username)
        cy.get('a#email').contains(email)
    })

    it('should be able to search user by email', () =>{
        cy.get('input[name="search"]').type(email)
        cy.get('form').submit()
        cy.contains(email)
        cy.contains(username)
    })

    it('should be able to search user by username', () =>{
        cy.get('input[name="search"]').type(username)
        cy.get('form').submit()
        cy.contains(email)
        cy.contains(username)
    })

    it('should logout when click logout button', () =>{
        cy.get('a.btn-primary').contains('Create New Project')
        cy.get('div#project-background > h3').contains('No Projects')
        cy.get('#logout').click()
        cy.url().should('include',"/accounts/login/")
    })
})