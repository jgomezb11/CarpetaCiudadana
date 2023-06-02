import Login from './Pages/Login/Login';
import Home from './Pages/Home/Home';
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
function App() {
  const router = createBrowserRouter([
    {
      path: '/',
      element: <Login />,
      errorElement: <h1>Error de ruta</h1>
    },
    {
      path: '/home',
      element: <Home />
    }
  ]);
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
