// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('register', (email, username, password)=>{
    cy.visit('/accounts/register/')
    cy.get('input[name="email"]').type(email)
    cy.get('input[name="username"]').type(username)
    cy.get('select').select('[Default Company]')
    cy.get('input[name="password1"]').type(password)
    cy.get('input[name="password2"]').type(password)
    cy.get('form').submit()

    cy.get('a#sign-in-link').should('exist')
})

Cypress.Commands.add('login', (username, password) => {
    cy.visit('/accounts/login/')
    cy.get('input[name="username"]').type(username)
    cy.get('input[name="password"]').type(password)
    cy.get('form').submit()
    // assert was able to login
    cy.getCookie("sessionid").should("exist");
})

Cypress.Commands.add('createProject', (projectName, duration, username) =>{

    cy.get('a.btn-primary').contains('Create New Project').click()
    cy.url().should('include',"/project/create/")

    cy.get('input[name="name"]').type(projectName)
    cy.get('input[name="duration"]').type(duration)
    cy.get('select').select(username)
    cy.get('input[type="submit"]').click()

    cy.contains('Successfully Created a New Project!')
    cy.get('a#go-home').click()

    cy.get('h4.project-name').contains(projectName)
    cy.get(`img[alt="@${username}"]`).should('exist')
})