import { useState } from 'react';
import './PassengerForm.css';

const PassengerForm = ({ onSubmit, initialData = null }) => {
  const [formData, setFormData] = useState({
    firstName: initialData?.nid?.Fname || '',
    lastName: initialData?.nid?.Lname || '',
    nationalId: initialData?.nid?.FAN || '',
    phoneNumber: initialData?.phone_number || '',
    emergencyContactName: initialData?.emergency_contact_name || '',
    emergencyContactPhone: initialData?.emergency_contact_phone || '',
    address: initialData?.nid?.Address || '',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    // National ID validation (exactly 12 digits)
    if (!/^\d{12}$/.test(formData.nationalId)) {
      newErrors.nationalId = 'National ID must be exactly 12 digits';
    }

    // Phone number validation (starts with 0, 10 digits)
    if (!/^0\d{9}$/.test(formData.phoneNumber)) {
      newErrors.phoneNumber = 'Phone number must start with 0 and be 10 digits long';
    }

    // Emergency contact phone validation (starts with 0, 10 digits)
    if (!/^0\d{9}$/.test(formData.emergencyContactPhone)) {
      newErrors.emergencyContactPhone = 'Emergency contact phone must start with 0 and be 10 digits long';
    }

    // Name validations (letters only)
    if (!/^[A-Za-z\s]+$/.test(formData.firstName)) {
      newErrors.firstName = 'First name must contain only letters';
    }

    if (!/^[A-Za-z\s]+$/.test(formData.lastName)) {
      newErrors.lastName = 'Last name must contain only letters';
    }

    if (!/^[A-Za-z\s]+$/.test(formData.emergencyContactName)) {
      newErrors.emergencyContactName = 'Emergency contact name must contain only letters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    let formattedValue = value;

    // Handle different input types
    switch (name) {
      case 'phoneNumber':
      case 'emergencyContactPhone':
        // Format phone numbers (start with 0, numbers only)
        if (!value.startsWith('0')) {
          formattedValue = '0' + value.replace(/^0/, '');
        }
        formattedValue = formattedValue.replace(/\D/g, '').slice(0, 10);
        break;

      case 'nationalId':
        // Numbers only for National ID and limit to 12 digits
        formattedValue = value.replace(/\D/g, '').slice(0, 12);
        break;

      case 'firstName':
      case 'lastName':
      case 'emergencyContactName':
        // Letters only for names
        formattedValue = value.replace(/[^A-Za-z\s]/g, '');
        break;

      default:
        formattedValue = value;
    }

    setFormData(prev => ({
      ...prev,
      [name]: formattedValue
    }));

    // Clear error when user is typing
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
        phone_number: formData.phoneNumber,
        emergency_contact_name: formData.emergencyContactName,
        emergency_contact_phone: formData.emergencyContactPhone
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="passenger-form">
      <div className="form-group">
        <label htmlFor="firstName">First Name*</label>
        <input
          type="text"
          id="firstName"
          name="firstName"
          value={formData.firstName}
          onChange={handleChange}
          className={errors.firstName ? 'error' : ''}
          placeholder="Enter letters only"
          required
        />
        {errors.firstName && <span className="error-message">{errors.firstName}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="lastName">Last Name</label>
        <input
          type="text"
          id="lastName"
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          className={errors.lastName ? 'error' : ''}
          placeholder="Enter letters only"
        />
        {errors.lastName && <span className="error-message">{errors.lastName}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="nationalId">National ID</label>
        <input
          type="text"
          id="nationalId"
          name="nationalId"
          value={formData.nationalId}
          onChange={handleChange}
          maxLength={12}
          className={errors.nationalId ? 'error' : ''}
          placeholder="Enter 12 digit number"
        />
        {errors.nationalId && <span className="error-message">{errors.nationalId}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="phoneNumber">Phone Number</label>
        <input
          type="text"
          id="phoneNumber"
          name="phoneNumber"
          value={formData.phoneNumber}
          onChange={handleChange}
          maxLength={10}
          className={errors.phoneNumber ? 'error' : ''}
          placeholder="Start with 0 (10 digits)"
        />
        {errors.phoneNumber && <span className="error-message">{errors.phoneNumber}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="emergencyContactName">Emergency Contact Name</label>
        <input
          type="text"
          id="emergencyContactName"
          name="emergencyContactName"
          value={formData.emergencyContactName}
          onChange={handleChange}
          className={errors.emergencyContactName ? 'error' : ''}
          placeholder="Enter letters only"
        />
        {errors.emergencyContactName && <span className="error-message">{errors.emergencyContactName}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="emergencyContactPhone">Emergency Contact Phone Number</label>
        <input
          type="text"
          id="emergencyContactPhone"
          name="emergencyContactPhone"
          value={formData.emergencyContactPhone}
          onChange={handleChange}
          maxLength={10}
          className={errors.emergencyContactPhone ? 'error' : ''}
          placeholder="Start with 0 (10 digits)"
        />
        {errors.emergencyContactPhone && <span className="error-message">{errors.emergencyContactPhone}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="address">Address</label>
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