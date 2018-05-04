import { store } from 'react-easy-state'

const SearchStore = store({
    sort: 'popular',

})

// stores behave like normal JS objects
// user.name = 'Bob'

export default SearchStore
