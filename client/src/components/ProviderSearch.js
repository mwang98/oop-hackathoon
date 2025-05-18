import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Card, Col, Row, Spinner } from 'react-bootstrap';
import providerService from '../services/providerService';

const ProviderSearch = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    zipCode: '94118',
    medicareNumber: '7G91HP2Q3R4',
    symptomDescription: 'I have a persistent cough and difficulty breathing.',
    availability: '05-20 14:00-16:00',
    name: 'John Doe',
    insuranceCompany: 'Medicare'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Use the provider service to make the API call
      const results = await providerService.getProviderRecommendations(formData);
      
      // Navigate to results page with the data
      navigate('/results', { state: { results } });
    } catch (error) {
      console.error('Error fetching provider recommendations:', error);
      alert('Error fetching provider recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Card className="shadow-sm">
        <Card.Header className="bg-light">
          <h2>Find Medicare Providers</h2>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Row className="mb-3">
              <Col md={6}>
                <Form.Group controlId="zipCode">
                  <Form.Label>ZIP Code</Form.Label>
                  <Form.Control
                    type="text"
                    name="zipCode"
                    placeholder="Enter your ZIP code"
                    value={formData.zipCode}
                    onChange={handleChange}
                    required
                    pattern="[0-9]{5}"
                  />
                  <Form.Text className="text-muted">
                    Enter a valid 5-digit ZIP code
                  </Form.Text>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group controlId="medicareNumber">
                  <Form.Label>Medicare Number</Form.Label>
                  <Form.Control
                    type="text"
                    name="medicareNumber"
                    placeholder="Enter your Medicare number"
                    value={formData.medicareNumber}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3" controlId="symptomDescription">
              <Form.Label>Describe Your Symptoms</Form.Label>
              <Form.Control
                as="textarea"
                name="symptomDescription"
                rows={3}
                placeholder="Describe your symptoms or health concerns"
                value={formData.symptomDescription}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="availability">
              <Form.Label>Your Availability</Form.Label>
              <Form.Control
                type="text"
                name="availability"
                placeholder="e.g., Weekdays 9am-5pm, Weekends 10am-2pm"
                value={formData.availability}
                onChange={handleChange}
                required
              />
              <Form.Text className="text-muted">
                Specify your preferred days and times for appointments
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" controlId="name">
              <Form.Label>Your Name</Form.Label>
              <Form.Control
                type="text"
                name="name"
                placeholder="Enter your name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <div className="d-grid gap-2">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" className="me-2" />
                    Searching...
                  </>
                ) : 'Find Providers'}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
};

export default ProviderSearch;
