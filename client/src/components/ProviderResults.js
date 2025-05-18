import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, Button, Row, Col, Badge, ListGroup } from 'react-bootstrap';

const ProviderResults = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const results = location.state?.results || [];

  const handleBack = () => {
    navigate('/');
  };

  if (!results.length) {
    return (
      <div className="text-center my-5">
        <h3>No provider results found</h3>
        <p>Please try again with different search criteria.</p>
        <Button variant="primary" onClick={handleBack}>
          Back to Search
        </Button>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Provider Results</h2>
        <Button variant="outline-primary" onClick={handleBack}>
          New Search
        </Button>
      </div>

      {results.map((recommendation, index) => (
        <Card key={index} className="mb-4 shadow-sm">
          <Card.Header className="bg-light">
            <h3>{recommendation.specialty || 'Medical Provider'}</h3>
            {recommendation.confidence && (
              <Badge bg="info">{recommendation.confidence} Match</Badge>
            )}
          </Card.Header>
          <Card.Body>
            {recommendation.reasoning && (
              <div className="mb-3">
                <h5>Why this specialty?</h5>
                <p>{recommendation.reasoning}</p>
              </div>
            )}

            <h5>Available Providers</h5>
            <Row>
              {recommendation.provider_infos && recommendation.provider_confirmation_infos && 
               recommendation.provider_infos.map((provider, idx) => {
                const confirmationInfo = recommendation.provider_confirmation_infos[idx];
                
                // Skip providers without confirmation info
                if (!confirmationInfo) return null;
                
                return (
                  <Col key={provider.id || idx} md={6} lg={4} className="mb-3">
                    <Card className="h-100">
                      <Card.Header className="d-flex justify-content-between">
                        <div>
                          <strong>{provider.name || `${provider.first_name} ${provider.last_name}`}</strong>
                        </div>
                        <Badge bg={confirmationInfo.is_in_network ? "success" : "warning"}>
                          {confirmationInfo.is_in_network ? "In Network" : "Out of Network"}
                        </Badge>
                      </Card.Header>
                      <Card.Body>
                        {provider.physician && (
                          <div className="mb-2">
                            <small>
                              {provider.physician.addressLine1}, {provider.physician.addressCity}, {provider.physician.addressState} {provider.physician.addressZipcode}
                            </small>
                            {provider.physician.phone && <p><small>Phone: {provider.physician.phone}</small></p>}
                          </div>
                        )}
                        
                        <h6>Available Time Slots:</h6>
                        {confirmationInfo.available_timeslot && confirmationInfo.available_timeslot.length > 0 ? (
                          <ListGroup className="mb-3">
                            {confirmationInfo.available_timeslot.map((slot, slotIdx) => (
                              <ListGroup.Item key={slotIdx} action className="py-2">
                                {slot}
                              </ListGroup.Item>
                            ))}
                          </ListGroup>
                        ) : (
                          <p className="text-muted">No available time slots</p>
                        )}
                        
                        {confirmationInfo.error && (
                          <div className="text-danger mt-2">
                            <small>{confirmationInfo.error}</small>
                          </div>
                        )}
                      </Card.Body>
                      <Card.Footer>
                        <Button variant="primary" size="sm" className="w-100">
                          Book Appointment
                        </Button>
                      </Card.Footer>
                    </Card>
                  </Col>
                );
              })}
            </Row>
          </Card.Body>
        </Card>
      ))}
    </div>
  );
};

export default ProviderResults;
