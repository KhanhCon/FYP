import { store } from 'react-easy-state'

const TopLibrariesStore = store({
    urlTopLibraries: 'http://127.0.0.1:5000/top',
    firstShaDate:'',
    date: '',
    libraries: []
})

// stores behave like normal JS objects
// user.name = 'Bob'

export default TopLibrariesStore
