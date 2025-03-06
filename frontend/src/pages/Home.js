console.log("Home.js chargé !");

import React from "react";
import { Link } from "react-router-dom";

function Home() {
  const modules = [
    { name: "Patch Notes Analyzer", path: "/patch-notes", description: "Génération et analyse des patch notes." },
    { name: "Autre Module", path: "#", description: "Futur module à intégrer." }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-gray-800 mb-2">Bienvenue sur l'application</h1>
        <p className="text-gray-600 text-lg">Sélectionnez un module ci-dessous pour commencer.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
        {modules.map((module, index) => (
          <Link to={module.path} key={index} className="block p-6 bg-white border border-gray-300 rounded-lg shadow-lg hover:shadow-xl transition-transform transform hover:scale-105">
            <h2 className="text-2xl font-semibold text-gray-800">{module.name}</h2>
            <p className="text-gray-600 mt-2">{module.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Home;