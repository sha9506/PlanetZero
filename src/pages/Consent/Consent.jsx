import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Consent.css';

const Consent = () => {
  const [agreed, setAgreed] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (agreed) {
      navigate('/onboarding');
    }
  };

  return (
    <div className="consent-page">
      <div className="consent-container">
        <h1>Privacy & Data Consent</h1>
        <p className="subtitle">Before we continue, please review and accept our terms</p>
        
        <div className="consent-content">
          <h2>Data Collection</h2>
          <p>
            PlanetZero collects and processes certain personal and usage-related data to help
            you understand and reduce your environmental impact. The data we collect is
            strictly limited to what is necessary for providing accurate carbon footprint
            insights and sustainability recommendations.
          </p>

          <p>The types of data we may collect include:</p>
          <ul>
            <li>
              <strong>Transportation and travel data</strong> (such as commuting methods,
              distance traveled, or travel frequency) to estimate emissions from mobility.
            </li>
            <li>
              <strong>Energy consumption information</strong> (electricity, fuel, or resource
              usage) to calculate household or personal energy-related emissions.
            </li>
            <li>
              <strong>Lifestyle and consumption habits</strong> (such as food choices or
              shopping behavior) to assess environmental impact patterns.
            </li>
            <li>
              <strong>Location data (optional)</strong>, used only to improve accuracy of
              region-specific emission factors and recommendations. You may choose not to
              provide this data.
            </li>
          </ul>

          <h2>How We Use Your Data</h2>
          <p>
            The information you provide is used solely to support PlanetZero's mission of
            promoting sustainable living and environmental awareness. Specifically, your data
            helps us:
          </p>

          <ul>
            <li>
              <strong>Calculate your carbon footprint</strong> using scientifically accepted
              estimation methods.
            </li>
            <li>
              <strong>Provide personalized sustainability recommendations</strong> that help
              you reduce emissions and adopt eco-friendly habits.
            </li>
            <li>
              <strong>Generate insights and analytics</strong> to show trends, progress, and
              potential areas for improvement.
            </li>
            <li>
              <strong>Improve platform features and performance</strong> through anonymized
              and aggregated analysis.
            </li>
          </ul>

          <p>
            PlanetZero does <strong>not sell, rent, or trade</strong> your personal data to
            third parties.
          </p>

          <h2>Your Rights & Choices</h2>
          <p>
            We respect your control over your personal information. As a user of PlanetZero,
            you have the right to:
          </p>

          <ul>
            <li>
              <strong>Access your data</strong> and review the information you have shared.
            </li>
            <li>
              <strong>Modify or update your data</strong> to keep it accurate and current.
            </li>
            <li>
              <strong>Delete your data</strong> and request account removal at any time.
            </li>
            <li>
              <strong>Opt out of optional data collection</strong>, including location-based
              features, without losing access to core functionality.
            </li>
          </ul>

          <p>
            By continuing to use PlanetZero, you acknowledge that you understand and consent
            to the collection and use of your data as described above.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="consent-form">
          <div className="checkbox-group">
            <input
              type="checkbox"
              id="consent"
              checked={agreed}
              onChange={(e) => setAgreed(e.target.checked)}
            />
            <label htmlFor="consent">
              I agree to the collection and processing of my data as described above
            </label>
          </div>

          <button type="submit" className="btn btn-primary" disabled={!agreed}>
            Continue
          </button>
        </form>
      </div>
    </div>
  );
};

export default Consent;
