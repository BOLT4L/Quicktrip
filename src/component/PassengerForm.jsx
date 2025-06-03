import { useState } from 'react';
import './PassengerForm.css';

const PassengerForm = ({ onSubmit, initialData = null }) => {
  const [formData, setFormData] = useState({
    firstName: initialData?.nid?.Fname || '',
    lastName: initialData?.nid?.Lname || '',
    nationalId: initialData?.nid?.FAN || '',
    phoneNumber: initialData?.phone_number || '',
    address: initialData?.nid?.Address || '',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    // National ID validation (16 digits)
    if (!/^\d{16}$/.test(formData.nationalId)) {
      newErrors.nationalId = 'National ID must be exactly 16 digits';
    }

    // Phone number validation (+251 followed by 9 digits)
    if (!/^\+251\d{9}$/.test(formData.phoneNumber)) {
      newErrors.phoneNumber = 'Phone number must start with +251 followed by 9 digits';
    }

    // Name validations
    if (!/^[A-Za-z\s]{2,50}$/.test(formData.firstName)) {
      newErrors.firstName = 'First name must be 2-50 characters long and contain only letters';
    }

    if (!/^[A-Za-z\s]{2,50}$/.test(formData.lastName)) {
      newErrors.lastName = 'Last name must be 2-50 characters long and contain only letters';
    }

    // Address validation
    if (formData.address.trim().length < 5) {
      newErrors.address = 'Address must be at least 5 characters long';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    let formattedValue = value;

    // Format phone number to always include +251
    if (name === 'phoneNumber') {
      if (!value.startsWith('+251')) {
        formattedValue = '+251' + value.replace(/^\+251/, '');
      }
      // Remove any non-digit characters except the leading +
      formattedValue = formattedValue.replace(/[^\d+]/g, '');
    }

    // For national ID, only allow digits
    if (name === 'nationalId') {
      formattedValue = value.replace(/\D/g, '');
    }

    setFormData(prev => ({
      ...prev,
      [name]: formattedValue
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit({
        nid: {
          Fname: formData.firstName,
          Lname: formData.lastName,
          FAN: formData.nationalId,
          Address: formData.address
        },
        phone_number: formData.phoneNumber
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="passenger-form">
      <div className="form-group">
        <label htmlFor="firstName">First Name:</label>
        <input
          type="text"
          id="firstName"
          name="firstName"
          value={formData.firstName}
          onChange={handleChange}
          className={errors.firstName ? 'error' : ''}
        />
        {errors.firstName && <span className="error-message">{errors.firstName}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="lastName">Last Name:</label>
        <input
          type="text"
          id="lastName"
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          className={errors.lastName ? 'error' : ''}
        />
        {errors.lastName && <span className="error-message">{errors.lastName}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="nationalId">National ID:</label>
        <input
          type="text"
          id="nationalId"
          name="nationalId"
          value={formData.nationalId}
          onChange={handleChange}
          maxLength={16}
          className={errors.nationalId ? 'error' : ''}
          placeholder="Enter 16 digit number"
        />
        {errors.nationalId && <span className="error-message">{errors.nationalId}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="phoneNumber">Phone Number:</label>
        <input
          type="text"
          id="phoneNumber"
          name="phoneNumber"
          value={formData.phoneNumber}
          onChange={handleChange}
          className={errors.phoneNumber ? 'error' : ''}
          placeholder="+251"
        />
        {errors.phoneNumber && <span className="error-message">{errors.phoneNumber}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="address">Address:</label>
        <input
          type="text"
          id="address"
          name="address"
          value={formData.address}
          onChange={handleChange}
          className={errors.address ? 'error' : ''}
        />
        {errors.address && <span className="error-message">{errors.address}</span>}
      </div>

      <button type="submit" className="submit-button">
        {initialData ? 'Update Passenger' : 'Add Passenger'}
      </button>
    </form>
  );
};

export default PassengerForm; 