import axios from 'axios';

const API_URL = '/api/providers';

// Set up a default axios instance for our API
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProviderRecommendations = async (searchData) => {
  try {
    // Format the request data according to the backend schema
    const requestData = {
      zipCode: parseInt(searchData.zipCode),
      patientInfo: {
        name: searchData.name,
        policyNum: searchData.medicareNumber,
        insuranceCompany: searchData.insuranceCompany || 'Medicare',
        dateTimeRange: searchData.availability
      },
      symptomDescription: searchData.symptomDescription,
      radius: 25.0
    };

    const response = await api.post('/recommend', requestData);
    console.log("Number of providers found:", response.data.length);
    console.log("Provider recommendations:", response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching provider recommendations:', error);
    throw error;
  }
};

export default {
  getProviderRecommendations
};
