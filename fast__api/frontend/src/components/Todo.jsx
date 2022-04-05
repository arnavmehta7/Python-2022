import axios from 'axios'
const TodoItem = ({todo}) => {
    const DeleteTodoHandler = (title)=>{
        axios.delete(`http://localhost:8000/api/todo${title}`)
        .then(res=>console.log(res.data))
    }

    return (
        <div>
            <p>
                <span style={{ fontWeight: 'bold, underline' }}>{todo.title} : </span> {todo.description}
                <button onClick={() => DeleteTodoHandler(todo.title)} className="btn btn-outline-danger my-2 mx-2" style={{'borderRadius':'50px',}}>X</button>
                <hr></hr>
            </p>
        </div>
    )
}

export default TodoItem
