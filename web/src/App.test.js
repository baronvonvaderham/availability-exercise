import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import {shallow, configure, mount} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import NameForm from './components/NameForm.js';
import AvailabilitySchedule from './components/AvailabilitySchedule.js';
import Appointments from './components/Appointments.js';


const mockAdvisorIds = ["12345", "67890"];
const mockAdvisorTimes = [
  ["2019-07-16T23:00:00-04:00", "2019-07-16T22:00:00-04:00"],
  ["2019-07-16T23:00:00-04:00", "2019-07-16T22:00:00-04:00"]
];
const mockAppointments = [
  {"studentName": "Jane Doe", "advisorId": "12345", "advisorTime": "2019-07-16T23:00:00-04:00"},
  {"studentName": "John Doe", "advisorId": "12345", "advisorTime": "2019-07-16T22:00:00-04:00"}
  ];

it("renders without crashing", () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});

configure({adapter: new Adapter()});

it("renders all components", () => {
  const app = shallow(<App />);
  expect(app.find(NameForm).length).toBe(1);
  expect(app.find(AvailabilitySchedule).length).toBe(1);
  expect(app.find(Appointments).length).toBe(1);
});

it("correctly loads availability table from props", () => {
  const app = shallow(<AvailabilitySchedule
    availabilityAdvisorIds={mockAdvisorIds}
    availabilityTimes={mockAdvisorTimes}
    bookAppointment={() => {}}
  />);
});

it("correctly loads booked appointments table from props", () => {
  const app = shallow(<Appointments
    appointmentsData={mockAppointments}
  />);
});
