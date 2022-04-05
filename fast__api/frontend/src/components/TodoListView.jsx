import TodoItem from './Todo'

export default function TodoView({todoList}) {
    return (
        <div>
            <ul>
                {todoList.map(todo => <TodoItem todo={todo} />)}
            </ul>
        </div>
    )
}
