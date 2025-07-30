function Login() {
  return (
    <div className="max-w-md mx-auto mt-12 p-6">
      <h1 className="text-3xl font-bold mb-4 text-gray-800">Login Page</h1>
      <h2 className="text-lg text-gray-600">
        Or sign up here!{" "}
        <a href="/register" className="text-blue-600 hover:underline">
          Register
        </a>
      </h2>
    </div>
  );
}

export default Login;