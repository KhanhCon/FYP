import { store } from 'react-easy-state'

const navbar = store([
    {'name':"Project",'link':"/projects"},
    {'name':"Home",'link':"/home"},
])

// stores behave like normal JS objects
// user.name = 'Bob'

export default navbar
