import { useState, useEffect } from "react";
import axios from "axios";

function App() {

  // Login States
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);

  // User State
  const [userId, setUserId] = useState(
    localStorage.getItem("user_id") || ""
  );

  // PDF + Question States
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [loading, setLoading] = useState(false);

// Handle register
  const handleRegister = async () => {

  try {

    setLoading(true);

    const response = await axios.post(
      "https://multiuser-rag-chatbot.onrender.com/register",
      {
        username,
        password,
      }
    );

    if (response.data.error) {

      alert(response.data.error);

    } else {

      alert("Registration Successful");

      setIsRegister(false);

    }

  } catch (error) {

    console.error(error);

    alert("Register Failed");

  } finally {

    setLoading(false);

  }
};

  // ---------------- LOGIN ----------------

  const handleLogin = async () => {

    try {

      setLoading(true);

      const response = await axios.post(
        `https://multiuser-rag-chatbot.onrender.com/login?username=${username}&password=${password}`
      );

      const id = response.data.user_id;

      localStorage.setItem("user_id", id);

      setUserId(id);

      alert("Login Successful");

    } catch (error) {

      console.error(error);

      alert("Login Failed");

    } finally {

      setLoading(false);

    }
  };

  // ---------------- LOGOUT ----------------

  const handleLogout = () => {

    localStorage.removeItem("user_id");

    setUserId("");

    setAnswer("");
    setQuestion("");

  };

  // ---------------- UPLOAD PDF ----------------

  const handleUpload = async () => {

    if (!file) {
      alert("Select PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      setLoading(true);

      const response = await axios.post(
        `https://multiuser-rag-chatbot.onrender.com/upload-pdf?user_id=${userId}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert("PDF Uploaded");

      console.log(response.data);

    } catch (error) {

      console.error(error);

      alert("Upload Failed");

    } finally {

      setLoading(false);

    }
  };

  // ---------------- ASK QUESTION ----------------

  const handleAsk = async () => {

    if (!question) {
      alert("Enter Question");
      return;
    }

    try {

      setLoading(true);

      const response = await axios.post(
        "https://multiuser-rag-chatbot.onrender.com/ask",
        {
          question: question,
          user_id: userId,
        }
      );

      setAnswer(response.data.answer);

    } catch (error) {

      console.error(error);

      alert("Question Failed");

    } finally {

      setLoading(false);

    }
  };

  // ---------------- LOGIN PAGE ----------------

  if (!userId) {

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-8 rounded-2xl shadow-lg w-[400px]">

        <h1 className="text-3xl font-bold mb-6 text-center">

          {isRegister ? "Register" : "Login"}

        </h1>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full border p-3 rounded-lg mb-4"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border p-3 rounded-lg mb-6"
        />

        {
          isRegister ? (

            <button
              onClick={handleRegister}
              className="w-full bg-green-600 text-white py-3 rounded-lg mb-4"
            >
              Register
            </button>

          ) : (

            <button
              onClick={handleLogin}
              className="w-full bg-black text-white py-3 rounded-lg mb-4"
            >
              Login
            </button>

          )
        }

        <button
          onClick={() => setIsRegister(!isRegister)}
          className="text-blue-600 w-full"
        >

          {
            isRegister
              ? "Already have an account? Login"
              : "Create New Account"
          }

        </button>

      </div>

    </div>
  );
}

  // ---------------- MAIN APP ----------------

  return (

    <div className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="flex justify-between items-center mb-8">

          <h1 className="text-4xl font-bold">
            RAG PDF Chatbot
          </h1>

          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-5 py-2 rounded-lg"
          >
            Logout
          </button>

        </div>

        {/* Upload */}
        <div className="bg-white p-6 rounded-2xl shadow-md mb-6">

          <h2 className="text-2xl font-semibold mb-4">
            Upload PDF
          </h2>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full border p-3 rounded-lg mb-4"
          />

          <button
            onClick={handleUpload}
            className="bg-black text-white px-6 py-3 rounded-lg"
          >
            Upload PDF
          </button>

        </div>

        {/* Ask */}
        <div className="bg-white p-6 rounded-2xl shadow-md mb-6">

          <h2 className="text-2xl font-semibold mb-4">
            Ask Question
          </h2>

          <textarea
            placeholder="Ask something..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full border p-4 rounded-lg min-h-[150px] mb-4"
          />

          <button
            onClick={handleAsk}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg"
          >
            Ask
          </button>

        </div>

        {/* Loading */}
        {loading && (

          <div className="bg-yellow-100 p-4 rounded-lg mb-6">
            Loading...
          </div>

        )}

        {/* Answer */}
        {answer && (

          <div className="bg-white p-6 rounded-2xl shadow-md">

            <h2 className="text-2xl font-semibold mb-4">
              Answer
            </h2>

            <p className="leading-7 text-gray-700">
              {answer}
            </p>

          </div>

        )}

      </div>

    </div>
  );
}

export default App;