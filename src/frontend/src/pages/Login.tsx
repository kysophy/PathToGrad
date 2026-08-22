import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext'; 

import NotebookPage from "../components/NotebookPage";
import Doodle from "../components/Doodle";

import bunny from "../assets/Bunny.svg";
import lightning from "../assets/Lightning 1.svg";
import arrow2 from "../assets/Arrow 2.svg";
import blueStars from "../assets/Blue Stars.svg";
import yellowStars from "../assets/Yellow Stars.svg";
import flower1 from "../assets/FLower 1.svg";
import flower2 from "../assets/Flower 2.svg";
import flower3 from "../assets/Flower 3.svg";
import mediumOrangeFlower from "../assets/Medium Orange Flower.svg";
import smallOrangeFlower from "../assets/Small Orange Flower.svg";
import dbCloud1 from "../assets/DB Cloud 1.svg";
import dbCloud2 from "../assets/DB CLoud 2.svg";
import lbCloud1 from "../assets/LB Cloud 1.svg";

/**
 * Login
 * -----
 * Student sign-in screen for PathToGrad, styled as a page in a hand-drawn notebook.
 */
export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [studentId, setStudentId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(""); 

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); 
    setError('');

    if (studentId === "test") {
      login({
        id: "pathtograd",
        name: "Test User",
        role: "Student",
      });
      navigate('/student-dashboard');
      return;
    }

    try {
      // Send credentials to Dev D's backend API
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier: studentId, password }), 
      });

      if (!response.ok) {
        throw new Error("Invalid credentials");
      }

      // Extract the JSON body to find out the role
      const data = await response.json(); 

      const userData = {
        role: data.role,
        id: studentId, 
        name: data.name || "Student",
      };

      // Save the role into your React in-memory context
      login(userData);

      // Route them to the correct interface based on their database role
      if (userData.role === 'Student') navigate('/student-dashboard');
      else if (userData.role === 'Advisor') navigate('/advisor-dashboard');
      else if (userData.role === 'Admin') navigate('/admin-dashboard');
      else {
        throw new Error("Unknown role received");
      }

    } catch (err) {
      console.error(err);
      setError("Login failed. Please check your ID and Password.");
    }
  };

  return (
    <NotebookPage>
      {/* ---------- Background doodles (blurred, per source design) ---------- */}
      {/* top-left cluster */}
      <Doodle blurred src={mediumOrangeFlower} left="0%" top="0%" vw={3.75} minPx={30} maxPx={54} />
      <Doodle blurred src={flower1} left="7.9%" top="0%" vw={4.03} minPx={32} maxPx={58} />
      <Doodle blurred src={flower2} left="3.5%" top="5.5%" vw={7.99} minPx={60} maxPx={115} />
      <Doodle blurred src={mediumOrangeFlower} left="13.5%" top="4.8%" vw={7.71} minPx={58} maxPx={111} />
      <Doodle blurred src={smallOrangeFlower} left="0%" top="14.7%" vw={4.38} minPx={34} maxPx={63} />
      <Doodle blurred src={flower3} left="0%" top="24.6%" vw={6.46} minPx={48} maxPx={93} />
      <Doodle blurred src={smallOrangeFlower} left="0%" top="39%" vw={4.38} minPx={34} maxPx={63} className="opacity-60" />

      {/* top-right cluster */}
      <Doodle blurred src={yellowStars} left="74.4%" top="11.9%" vw={3.75} minPx={30} maxPx={54} />
      <Doodle blurred src={yellowStars} left="75.7%" top="1.5%" vw={6.81} minPx={52} maxPx={98} />
      <Doodle blurred src={blueStars} left="82.8%" top="0.2%" vw={10.76} minPx={80} maxPx={155} />
      <Doodle blurred src={blueStars} left="92.6%" top="11.3%" vw={7.08} minPx={54} maxPx={102} />
      <Doodle blurred src={flower1} left="86.1%" top="20.3%" vw={4.31} minPx={34} maxPx={62} />

      {/* right-middle cluster (below the lightning doodle) */}
      <Doodle blurred src={mediumOrangeFlower} left="94.1%" top="45.2%" vw={5.62} minPx={42} maxPx={81} />
      <Doodle blurred src={flower2} left="94.6%" top="60.6%" vw={4.03} minPx={30} maxPx={58} />
      <Doodle blurred src={smallOrangeFlower} left="93.3%" top="69.8%" vw={5.56} minPx={42} maxPx={80} />

      {/* bottom-right cluster */}
      <Doodle blurred src={flower3} left="74.1%" top="91.9%" vw={6.53} minPx={50} maxPx={94} />
      <Doodle blurred src={mediumOrangeFlower} left="85.2%" top="91.1%" vw={7.64} minPx={58} maxPx={110} />
      <Doodle blurred src={flower1} left="85.5%" top="75.6%" vw={7.92} minPx={60} maxPx={114} />
      <Doodle blurred src={flower2} left="93.9%" top="89.8%" vw={5.9} minPx={44} maxPx={85} />

     {/* Notebook-cover cloud bank, bottom-left corner (crisp, not blurred) */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute bottom-0 left-0 select-none"
        style={{ width: "53.7vw", maxWidth: "774px" }}
      >
        <img src={lbCloud1} alt="" className="absolute bottom-0 left-[8%] w-[70%]" />
        <img src={dbCloud1} alt="" className="absolute bottom-0 left-0 w-[55%]" />
        <img src={dbCloud2} alt="" className="absolute bottom-0 left-[38%] w-[35%]" />
      </div>

      {/* ---------- Card ---------- */}
      <div className="flex min-h-screen w-full items-center justify-center px-4 py-16 sm:px-8">
        
        {error && (
          <div className="absolute top-4 bg-red-200 text-red-800 p-2 rounded border border-red-400 font-quicksand z-50">
            {error}
          </div>
        )}
        
        <div className="relative w-full max-w-[36rem] origin-center animate-fade-in rounded-xl bg-[#D7D7D7] px-6 py-6 opacity-0 shadow-sm sm:px-10 sm:py-8">
          {/* Bunny doodle, pinned to the card's top-left corner (crisp) */}
          <img
            src={bunny}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute -left-6 -top-7 w-14 select-none sm:-left-7 sm:-top-8 sm:w-16"
          />

          {/* Lightning doodle, pinned to the card's right edge (crisp) */}
          <img
            src={lightning}
            alt=""
            aria-hidden="true"
            className="pointer-events-none absolute -right-5 top-1/2 w-8 -translate-y-1/2 rotate-6 select-none sm:-right-8 sm:w-10"
          />

          <h1 className="font-heading text-center text-4xl leading-[0.95] text-neutral-900 sm:text-5xl">
            PathTo
            <br />
            Grad
          </h1>

          <form onSubmit={handleSubmit} className="mt-8 flex flex-col gap-4 sm:mt-9">
            <label className="flex items-baseline gap-2 border-b-2 border-neutral-900 pb-1">
              <span className="font-body shrink-0 text-base text-neutral-900 sm:text-lg">
                ID
              </span>
              <input
                type="text"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="font-body w-full bg-transparent text-base text-neutral-900 outline-none sm:text-lg"
                autoComplete="username"
              />
            </label>

            <label className="flex items-baseline gap-2 border-b-2 border-neutral-900 pb-1">
              <span className="font-body shrink-0 text-base text-neutral-900 sm:text-lg">
                Password
              </span>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="font-body w-full bg-transparent text-base text-neutral-900 outline-none sm:text-lg"
                autoComplete="current-password"
              />
            </label>

            <div className="mt-2 flex flex-col items-center gap-2">
              <button
                type="submit"
                aria-label="Log in"
                className="rotate-90 transition-transform hover:scale-110 focus-visible:scale-110 focus-visible:outline-none"
              >
                <img src={arrow2} alt="" className="w-12 sm:w-14" />
              </button>

              <a
                href="/forgot-password"
                className="font-body text-sm text-neutral-800 underline-offset-2 hover:underline sm:text-base"
              >
                Forgot password
              </a>
            </div>
          </form>
        </div>
      </div>
    </NotebookPage>
  );
}