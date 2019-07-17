import React from 'react';

function Appointments(props) {
  return (
    <React.Fragment>
      <h2>Booked Times</h2>
        <table className="bookings table">
          <thead>
            <tr>
              <th>Advisor ID</th>
              <th>Student Name</th>
              <th>Date/Time</th>
            </tr>
          </thead>
          <tbody>
            {props.appointmentsData.map((appointment, index) => {
              let date = new Date(appointment.advisorTime);
              return (
                <tr key={index}>
                  <td className="booking-advisor-id">{appointment.advisorId}</td>
                  <td className="booking-student-name">{appointment.studentName}</td>
                  <td>
                    <time dateTime={appointment.advisorTime}>{date.toLocaleDateString()} {date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</time>
                  </td>
                </tr>
              )})}
          </tbody>
        </table>
    </React.Fragment>
  );
}
export default Appointments;