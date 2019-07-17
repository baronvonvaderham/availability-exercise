import React from 'react';

function AvailabilitySchedule(props) {
  return (
    <React.Fragment>
      <h2>Available Times</h2>
        <table className="advisors table">
          <thead>
            <tr>
              <th>Advisor ID</th>
              <th>Available Times</th>
            </tr>
          </thead>
          <tbody>
            {props.availabilityAdvisorIds.map((id, i) => (
              <tr key={id}>
                <td className="advisor-id">{id}</td>
                <td>
                  <ul className="list-unstyled">
                  {props.availabilityTimes[i].map((time, j) => {
                    let date = new Date(time);
                    return (
                      <li key={j}>
                        <time dateTime={time} className="book-time">{date.toLocaleDateString()} {date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</time>
                        <button
                          className="book btn-small btn-primary"
                          onClick={() => props.bookAppointment(id, time, i, j)}
                        >Book</button>
                      </li>
                  )})}
                  </ul>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
    </React.Fragment>
  );
}

export default AvailabilitySchedule;