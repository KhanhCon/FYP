import { store } from 'react-easy-state'

const TopLibrariesStore = store({
    urlTopLibraries: 'http://192.168.1.65:5000/top',
    date:'',
    libraries: []
})

// stores behave like normal JS objects
// user.name = 'Bob'

export default TopLibrariesStore
