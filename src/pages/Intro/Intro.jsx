import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaArrowRight } from 'react-icons/fa';
import IntroLogo from '../../assets/intro.svg';
import './Intro.css';

const Intro = () => {
  const navigate = useNavigate();

  const handleStart = () => {
    navigate('/landing');
  };

  return (
    <div className="intro-page">
      <div className="intro-container">
        <div className="intro-content">
          <p className="intro-tagline">Earth but upgraded.</p>
          
          <div className="intro-logo-wrapper">
            <img 
              src={IntroLogo}
              alt="Planet Zero Logo" 
              className="intro-logo-image"
            />
          </div>

          <button onClick={handleStart} className="intro-button">
            Let's Start <FaArrowRight className="button-arrow" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Intro;
