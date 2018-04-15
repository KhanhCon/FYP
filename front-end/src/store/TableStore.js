import { store } from 'react-easy-state'

const TableStore = store({
    date: '12',
    num: '',
    table: [],
})

// stores behave like normal JS objects
// user.name = 'Bob'

export default TableStore
