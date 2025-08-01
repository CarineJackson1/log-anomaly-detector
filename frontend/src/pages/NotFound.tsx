import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';


function NotFound () {

const navigate = useNavigate();

useEffect(() => {
    const timer = setTimeout(() => {
        navigate("/");
    }, 3000);

    return () => clearTimeout(timer); 
}, [navigate])

    return (
        <>
        <h1>404 Page:</h1>
        <p>Sorry, we were unable to locate the desired page. Redirecting in 3...2...1</p>
        </>
    );
}

export default NotFound;