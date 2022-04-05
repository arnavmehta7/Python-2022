
const l = 'http://127.0.0.1:8000/add/'

const fetchTodos = async () => {
   const response = await fetch("http://127.0.0.1:8000/")
   const todos = await response.json()
   console.log(todos.data)
}
fetchTodos()
