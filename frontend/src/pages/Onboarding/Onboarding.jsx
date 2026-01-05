import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaInfoCircle } from 'react-icons/fa';
import api from '../../services/api';
import './Onboarding.css';

const Onboarding = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    country: '',
    city: '',
    householdSize: 1,
    transportMode: '',
    dietType: '',
    energySource: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Country and city data
  const countries = [
    'United States',
    'Canada',
    'United Kingdom',
    'Australia',
    'Germany',
    'France',
    'Spain',
    'Italy',
    'Japan',
    'China',
    'India',
    'Brazil',
    'Mexico',
    'South Africa',
    'Netherlands',
    'Sweden',
    'Norway',
    'Denmark',
    'Switzerland',
    'Belgium',
    'Austria',
    'Portugal',
    'Greece',
    'Poland',
    'Ireland',
    'New Zealand',
    'Singapore',
    'South Korea',
    'Malaysia',
    'Thailand',
    'UAE',
    'Saudi Arabia',
    'Egypt',
    'Nigeria',
    'Kenya',
    'Argentina',
    'Chile',
    'Colombia',
    'Peru',
  ];

  const citiesByCountry = {
    'United States': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Francisco', 'Seattle', 'Boston', 'Miami', 'Atlanta', 'Denver'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa', 'Edmonton', 'Winnipeg', 'Quebec City', 'Hamilton', 'Victoria'],
    'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Edinburgh', 'Glasgow', 'Bristol', 'Leeds', 'Sheffield', 'Newcastle'],
    'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Canberra', 'Hobart', 'Darwin'],
    'Germany': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Stuttgart', 'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig'],
    'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille'],
    'Spain': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza', 'Málaga', 'Murcia', 'Palma', 'Bilbao', 'Alicante'],
    'Italy': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Venice', 'Verona'],
    'Japan': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya', 'Sapporo', 'Fukuoka', 'Kobe', 'Kyoto', 'Kawasaki', 'Hiroshima'],
    'China': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu', 'Hangzhou', 'Wuhan', 'Xi\'an', 'Chongqing', 'Tianjin'],
    'India': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat'],
    'Brazil': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre'],
    'Mexico': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana', 'León', 'Juárez', 'Zapopan', 'Mérida', 'Cancún'],
    'South Africa': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth', 'Bloemfontein', 'East London', 'Kimberley', 'Nelspruit'],
    'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen'],
    'Sweden': ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala', 'Västerås', 'Örebro', 'Linköping', 'Helsingborg', 'Jönköping', 'Norrköping'],
    'Norway': ['Oslo', 'Bergen', 'Trondheim', 'Stavanger', 'Drammen', 'Fredrikstad', 'Kristiansand', 'Sandnes', 'Tromsø', 'Sarpsborg'],
    'Denmark': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg', 'Randers', 'Kolding', 'Horsens', 'Vejle', 'Roskilde'],
    'Switzerland': ['Zurich', 'Geneva', 'Basel', 'Lausanne', 'Bern', 'Winterthur', 'Lucerne', 'St. Gallen', 'Lugano', 'Biel'],
    'Belgium': ['Brussels', 'Antwerp', 'Ghent', 'Charleroi', 'Liège', 'Bruges', 'Namur', 'Leuven', 'Mons', 'Aalst'],
    'Austria': ['Vienna', 'Graz', 'Linz', 'Salzburg', 'Innsbruck', 'Klagenfurt', 'Villach', 'Wels', 'Sankt Pölten', 'Dornbirn'],
    'Portugal': ['Lisbon', 'Porto', 'Braga', 'Funchal', 'Coimbra', 'Setúbal', 'Almada', 'Agualva-Cacém', 'Queluz', 'Amadora'],
    'Greece': ['Athens', 'Thessaloniki', 'Patras', 'Heraklion', 'Larissa', 'Volos', 'Rhodes', 'Ioannina', 'Chania', 'Chalcis'],
    'Poland': ['Warsaw', 'Kraków', 'Łódź', 'Wrocław', 'Poznań', 'Gdańsk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Katowice'],
    'Ireland': ['Dublin', 'Cork', 'Limerick', 'Galway', 'Waterford', 'Drogheda', 'Dundalk', 'Swords', 'Bray', 'Navan'],
    'New Zealand': ['Auckland', 'Wellington', 'Christchurch', 'Hamilton', 'Tauranga', 'Dunedin', 'Palmerston North', 'Napier', 'Porirua', 'New Plymouth'],
    'Singapore': ['Singapore'],
    'South Korea': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon', 'Gwangju', 'Suwon', 'Ulsan', 'Changwon', 'Goyang'],
    'Malaysia': ['Kuala Lumpur', 'George Town', 'Ipoh', 'Shah Alam', 'Petaling Jaya', 'Johor Bahru', 'Malacca City', 'Kota Kinabalu', 'Kuching', 'Seremban'],
    'Thailand': ['Bangkok', 'Chiang Mai', 'Phuket', 'Pattaya', 'Nakhon Ratchasima', 'Hat Yai', 'Udon Thani', 'Khon Kaen', 'Nakhon Si Thammarat', 'Surat Thani'],
    'UAE': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Ajman', 'Ras Al Khaimah', 'Fujairah', 'Umm Al Quwain'],
    'Saudi Arabia': ['Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam', 'Khobar', 'Tabuk', 'Buraidah', 'Khamis Mushait', 'Abha'],
    'Egypt': ['Cairo', 'Alexandria', 'Giza', 'Shubra El Kheima', 'Port Said', 'Suez', 'Luxor', 'Aswan', 'Mansoura', 'Tanta'],
    'Nigeria': ['Lagos', 'Kano', 'Ibadan', 'Abuja', 'Port Harcourt', 'Benin City', 'Kaduna', 'Maiduguri', 'Zaria', 'Aba'],
    'Kenya': ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 'Malindi', 'Kitale', 'Garissa', 'Kakamega'],
    'Argentina': ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata', 'Mar del Plata', 'Salta', 'San Juan', 'Santa Fe', 'San Miguel de Tucumán'],
    'Chile': ['Santiago', 'Valparaíso', 'Concepción', 'La Serena', 'Antofagasta', 'Temuco', 'Rancagua', 'Talca', 'Arica', 'Puerto Montt'],
    'Colombia': ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Cúcuta', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Ibagué'],
    'Peru': ['Lima', 'Arequipa', 'Trujillo', 'Chiclayo', 'Piura', 'Iquitos', 'Cusco', 'Huancayo', 'Tacna', 'Ica'],
  };

  const availableCities = formData.country ? citiesByCountry[formData.country] || [] : [];

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Reset city when country changes
    if (name === 'country') {
      setFormData({
        ...formData,
        country: value,
        city: '',
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleNext = async () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      // Save onboarding data to backend
      setIsLoading(true);
      setError('');
      
      try {
        console.log('Submitting onboarding data:', formData);
        
        // Update profile with onboarding data
        await api.completeOnboarding({
          country: formData.country,
          city: formData.city,
          // Store additional onboarding preferences in profile
          household_size: formData.householdSize,
          transport_mode: formData.transportMode,
          diet_type: formData.dietType,
          energy_source: formData.energySource,
        });
        
        console.log('Onboarding complete, navigating to dashboard');
        navigate('/dashboard');
      } catch (err) {
        console.error('Onboarding error:', err);
        setError(err.message || 'Failed to save onboarding data. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  return (
    <div className="onboarding-page">
      <div className="onboarding-container">
        <div className="progress-bar">
          <div className="progress" style={{ width: `${(step / 3) * 100}%` }}></div>
        </div>

        <h1>Let's Get Started</h1>
        <p className="subtitle">Step {step} of 3</p>

        {error && (
          <div className="error-message" style={{
            padding: '1rem',
            marginBottom: '1.5rem',
            backgroundColor: '#fee',
            border: '1px solid #fcc',
            borderRadius: '8px',
            color: '#c33',
            textAlign: 'center'
          }}>
            ❌ {error}
          </div>
        )}

        {step === 1 && (
          <div className="onboarding-step">
            <h2>Basic Information</h2>
            <div className="form-group">
              <label htmlFor="country">Country</label>
              <select
                id="country"
                name="country"
                value={formData.country}
                onChange={handleChange}
              >
                <option value="">Select your country...</option>
                {countries.map((country) => (
                  <option key={country} value={country}>
                    {country}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="city">City</label>
              <select
                id="city"
                name="city"
                value={formData.city}
                onChange={handleChange}
                disabled={!formData.country}
              >
                <option value="">
                  {formData.country ? 'Select your city...' : 'Select a country first'}
                </option>
                {availableCities.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </select>
              {!formData.country && (
                <small className="field-hint">Please select a country first</small>
              )}
            </div>
            <div className="form-group">
              <label htmlFor="householdSize">Household Size</label>
              <input
                type="number"
                id="householdSize"
                name="householdSize"
                value={formData.householdSize}
                onChange={handleChange}
                min="1"
                max="20"
              />
              <small className="field-hint">Number of people living in your household</small>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="onboarding-step">
            <h2>Transportation & Diet</h2>
            <div className="form-group">
              <label htmlFor="transportMode">Primary Transport Mode</label>
              <select
                id="transportMode"
                name="transportMode"
                value={formData.transportMode}
                onChange={handleChange}
              >
                <option value="">Select...</option>
                <option value="car">Car</option>
                <option value="public">Public Transport</option>
                <option value="bike">Bike/Walk</option>
                <option value="mixed">Mixed</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="dietType">Diet Type</label>
              <select
                id="dietType"
                name="dietType"
                value={formData.dietType}
                onChange={handleChange}
              >
                <option value="">Select...</option>
                <option value="omnivore">Omnivore</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="pescatarian">Pescatarian</option>
              </select>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="onboarding-step">
            <h2>Energy & Goals</h2>
            <div className="form-group">
              <label htmlFor="energySource">
                Primary Energy Source
                <span className="info-tooltip">
                  <FaInfoCircle className="info-icon" />
                  <span className="tooltip-text">
                    This refers to how electricity is generated in your area. Renewable sources include solar, wind, and hydro power. Mixed grid uses a combination of renewable and fossil fuels. If you're unsure, check your utility bill or select 'Don't Know'.
                  </span>
                </span>
              </label>
              <select
                id="energySource"
                name="energySource"
                value={formData.energySource}
                onChange={handleChange}
              >
                <option value="">Select...</option>
                <option value="renewable">Renewable (Solar, Wind, Hydro)</option>
                <option value="mixed">Mixed Grid (Combination)</option>
                <option value="fossil">Fossil Fuels (Coal, Gas, Oil)</option>
                <option value="unknown">Don't Know</option>
              </select>
              <small className="field-hint">The type of energy used to power your home</small>
            </div>
          </div>
        )}

        <div className="button-group">
          {step > 1 && (
            <button onClick={handleBack} className="btn btn-secondary" disabled={isLoading}>
              Back
            </button>
          )}
          <button onClick={handleNext} className="btn btn-primary" disabled={isLoading}>
            {isLoading ? 'Saving...' : (step === 3 ? 'Complete' : 'Next')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Onboarding;
