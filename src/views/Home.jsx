import React, { useContext } from 'react'
import { Context } from "../js/store/appContext.jsx"

const Home = () => {

  const { store } = useContext(Context)

  return (
    <div>
      Home
      <h5>Personas en global:{store.personas}</h5>
    </div>
  )
}

export default Home