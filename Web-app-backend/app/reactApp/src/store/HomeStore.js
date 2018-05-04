import { store } from 'react-easy-state'

const homeStore = store({
    PHP:{
        language:"PHP",
        mostPopularProjects:[]
    }
})

// stores behave like normal JS objects
// user.name = 'Bob'

export default homeStore
