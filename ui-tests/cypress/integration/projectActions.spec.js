const faker = require('faker');
function toTitleCase(str) {
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}

context('Project Actions', ()=>{
    let email, username, password;
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

    it('should be able to create a project by clicking new project button', ()=>{
        cy.get('a.btn-primary').contains('Create New Project').click()
        cy.url().should('include',"/project/create/")
    })

    it('should be able to create a project by clicking new project button', ()=>{
        cy.get('a#create-a-project').click()
        cy.url().should('include',"/project/create/")
    })

    it('should be able to create a project successfully', ()=>{
        const projectName = faker.lorem.words()
        cy.createProject(projectName, 1, username)
    })

    it('should be able to view project successfully', ()=>{
        const projectName = toTitleCase(faker.lorem.words())
        cy.createProject(projectName, 3, username)
        cy.get('a.project-content-text').first().click()
        cy.get('#project-name').contains(projectName)
        cy.contains(`3 weeks long`)
        cy.contains(username)

        // number of weeks rows
        cy.get('table').find('.week-header').its('length').should('eq', 3)
        // number of weeks rows
        cy.get('table').find('.group-header').its('length').should('eq', 1)
    })
    it('should be able to invite a user and be in a project together', () =>{
        const secondUsername = faker.internet.userName()
        const secondEmail = faker.internet.email()
        cy.get('a#invite-a-teammate').click()
        cy.get('input[name="username"]').type(secondUsername)
        cy.get('input[name="email"]').type(secondEmail)
        cy.get('input[type="submit"]').click()

        cy.contains("Successfully invited a new Teammate!")

        cy.get('a#create-a-project').click()

        const projectName = toTitleCase(faker.lorem.words())
        cy.url().should('include',"/project/create/")

        cy.get('input[name="name"]').type(projectName)
        cy.get('input[name="duration"]').type(1)
        cy.get('select').select([username, secondUsername])
        cy.get('input[type="submit"]').click()


        cy.contains('Successfully Created a New Project!')
        cy.get('a#go-home').click()

        cy.get('h4.project-name').contains(projectName)
        cy.get(`img[alt="@${username}"]`).should('exist')

        cy.get('a.project-content-text').first().click()

        cy.contains(username)
        cy.contains(secondUsername)


        // number of weeks rows
        cy.get('table').find('.week-header').its('length').should('eq', 1)
        // number of weeks rows
        cy.get('table').find('.group-header').its('length').should('eq', 1)
    })
})