import React, { Component } from 'react';
import axios from 'axios';
import NameForm from './components/NameForm.js';
import AvailabilitySchedule from './components/AvailabilitySchedule.js';
import Appointments from './components/Appointments.js';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      today: null,
      studentName: null,
      availabilityAdvisorIds: [],
      availabilityTimes: [],
      appointmentsData: [],
    };
    this.onNameChange = this.onNameChange.bind(this);
    this.bookAppointment = this.bookAppointment.bind(this);
  }

  onNameChange(e) {
    this.setState({
      studentName: e.target.value
    });
  }

  componentDidMount() {
    let availabilitySchedulePromise = axios.get("http://localhost:4433/availability-schedule")
      .catch((err) => {
        console.error("Error retrieving Availability Schedule data.", err);
      });

    let appointmentsPromise = axios.get("http://localhost:4433/booked-appointments")
      .catch((err) => {
        console.error("Error retrieving Booked Appointments data.", err);
      });

    let todayPromise = axios.get("http://localhost:4433/today")
      .catch((err) => {
        console.error("Error retrieving Current Date.")
      });

    Promise.all([availabilitySchedulePromise, appointmentsPromise, todayPromise])
      .then((results) => {
        this.setState({
          availabilityAdvisorIds: results[0].data.advisor_ids,
          availabilityTimes: results[0].data.advisor_times,
          appointments: results[1].data,
          today: new Date(results[2].data.today).toLocaleDateString(),
        });
      });
  }

  bookAppointment(advisorId, advisorTime, i, j) {
    // NOTATION: i is the index of the advisorId in that list, j is the index of the advisorTime in that list
    if (!this.state.studentName) {
      alert('Student name is required to schedule an appointment.')
    } else {
      let appointment = {
        advisorId: advisorId,
        advisorTime: advisorTime,
        studentName: this.state.studentName,
      };
      axios.post("http://localhost:4433/book-appointment", {appointment: appointment});

      // Add to the appointments data table
      let appointmentsData = [...this.state.appointmentsData, appointment];

      // Remove from the availability table, then delete any advisors who now have zero slots left
      let availabilityTimes = this.state.availabilityTimes;
      let availabilityAdvisorIds = this.state.availabilityAdvisorIds;
      availabilityTimes[i].splice(j, 1);
      if (availabilityTimes[i].length === 0) {
        availabilityAdvisorIds.splice(i, 1);
        availabilityTimes.splice(i, 1);
      }

      // Now just update the state to display all the changes!
      this.setState({
        availabilityAdvisorIds: availabilityAdvisorIds,
        availabilityTimes: availabilityTimes,
        appointmentsData: appointmentsData,
      });
    }
  }

  render() {
    return (
      <div className="App container">
        <NameForm
          today={this.state.today}
          onNameChange={this.onNameChange}
        />
        <AvailabilitySchedule
          availabilityAdvisorIds={this.state.availabilityAdvisorIds}
          availabilityTimes={this.state.availabilityTimes}
          bookAppointment={this.bookAppointment}
        />
        <Appointments
          appointmentsData={this.state.appointmentsData}
        />
      </div>
    );
  }
}

export default App;
