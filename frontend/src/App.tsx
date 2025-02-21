import React, { useState } from 'react';

function App() {
  const [userInput, setUserInput] = useState({
    startDate: '',
    endDate: '',
    repeatNum: 1,
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setUserInput((prev) => ({
      ...prev,
      [name]: name === 'repeatNum' ? Number(value) : value,
    }));
  };

  const handleClick = async (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    // event.preventDefault();
    // console.log(userInput);
    const response = await fetch('http://localhost:8000/generate-excel', {
      method: 'POST',
      headers: {
        'Content-Type': 'appilcation/json',
      },
      body: JSON.stringify(userInput),
    });

    console.log(response);

    if (response.ok) {
      console.log(response.status);
    } else {
      console.log('Failed to create a file', response);
    }
  };

  return (
    <>
      <div>
        <h1>Date Weaver</h1>
      </div>

      <form action=''>
        <input
          type='date'
          name='startDate'
          value={userInput.startDate}
          onChange={handleChange}
          required
        />
        <input
          type='date'
          name='endDate'
          value={userInput.endDate}
          onChange={handleChange}
          required
        />
        <input
          type='number'
          name='repeatNum'
          value={userInput.repeatNum}
          onChange={handleChange}
          required
        />
        <button onClick={handleClick}>Create a file</button>
      </form>
    </>
  );
}

export default App;
