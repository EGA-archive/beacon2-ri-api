import './SignUpForm.css'
import { NavLink } from 'react-router-dom';
import { Router, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Route, Routes } from 'react-router-dom';
import { Component } from 'react';
import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';

const apiURL = 'http://localhost:8080/auth/admin/realms/Beacon/users'
const apiURL2 = 'http://localhost:8080/auth/realms/Beacon/protocol/openid-connect/token'


class SignUpForm extends Component {

    constructor() {
        super();

        this.state = {
            email: "",
            password: "",
            userName: "",
            name: "",
            surname: "",
            error: ""
        };

        this.handleChange = this.handleChange.bind(this);


    }


    handleChange(event) {
        let target = event.target;
        let value = target.type === "checkbox" ? target.checked : target.value;
        let name = target.name;

        this.setState({
            [name]: value
        });
    }


    handleChange(event) {
        let target = event.target;
        let value = target.type === "checkbox" ? target.checked : target.value;
        let name = target.name;

        this.setState({
            [name]: value
        });
    }


    handleSubmit = async (e) => {

        e.preventDefault();

        const resp = await fetch(apiURL2, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'grant_type=client_credentials&client_id=admin-cli&client_secret=QOzMITQmtaoDrOenXu38pyDq2x0feCoO'

        })

        const response2 = await resp.json()
        console.log(response2)
        console.log(response2.access_token)


        const yourNewData = {
            "firstName": this.state.name,
            "lastName": this.state.surname,
            "email": this.state.email,
            "enabled": "true",
            "username": this.state.userName,
            "credentials": [{ "type": "password", "value": this.state.password, "temporary": false }],

        }
        console.log(yourNewData)

        const response = await fetch(apiURL, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json;charset=UTF-8',
                'Authorization': `Bearer ${response2.access_token}`, // notice the Bearer before your token
            },
            body: JSON.stringify(yourNewData)
        })
        console.log(response)


        if (response.status === 409) {

            this.setState({
                ["error"]: "This username already exsists. Please try with a different one"
            });

        }

        const permissionsRes = await fetch(
            "http://localhost:5051/", {
            method: 'POST',
            headers: {
                'Content-type': 'application/json;',
                'Authorization': `Bearer ${response2.access_token}`, // notice the Bearer before your token
            },
        })
        console.log(permissionsRes)

    }


    render() {
        return (
            <div className="login">
                <div className="appAside" />
                <div className="appForm">
                    <div className="pageSwitcher">

                        <NavLink

                            to="/sign-up"
                            className={(element) => element.isActive ? 'formTitleLink' : 'formTitleLink-active'}
                        >
                            Sign Up
                        </NavLink>
                        <NavLink
                            to="/sign-in"
                            className={(element) => element.isActive ? 'formTitleLink' : 'formTitleLink-active'}
                        >
                            Sign In
                        </NavLink>
                    </div>

                    <div className="formCenter">
                        <form className="formFields" onSubmit={this.handleSubmit}>
                            <div className="formField">
                                <label className="formFieldLabel" htmlFor="name">
                                    Name
                                </label>
                                <input
                                    type="name"
                                    id="name"
                                    className="formFieldInput"
                                    placeholder="Enter your name"
                                    name="name"
                                    value={this.state.name}
                                    onChange={this.handleChange}
                                />
                            </div>
                            <div className="formField">
                                <label className="formFieldLabel" htmlFor="surname">
                                    Surname
                                </label>
                                <input
                                    type="surname"
                                    id="surname"
                                    className="formFieldInput"
                                    placeholder="Enter your surname"
                                    name="surname"
                                    value={this.state.surname}
                                    onChange={this.handleChange}
                                />
                            </div>
                            <div className="formField">
                                <label className="formFieldLabel" htmlFor="userName">
                                    Username
                                </label>
                                {this.state.error !== '' && <h3>{this.state.error}</h3>}
                                <input
                                    type="username"
                                    id="username"
                                    className="formFieldInput"
                                    placeholder="Enter your username"
                                    name="userName"
                                    value={this.state.userName}
                                    onChange={this.handleChange}
                                />
                            </div>
                            <div className="formField">
                                <label className="formFieldLabel" htmlFor="email">
                                    E-Mail Address
                                </label>
                                <input
                                    type="email"
                                    id="email"
                                    className="formFieldInput"
                                    placeholder="Enter your email"
                                    name="email"
                                    value={this.state.email}
                                    onChange={this.handleChange}
                                />
                            </div>

                            <div className="formField">
                                <label className="formFieldLabel" htmlFor="password">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    id="password"
                                    className="formFieldInput"
                                    placeholder="Enter your password"
                                    name="password"
                                    value={this.state.password}
                                    onChange={this.handleChange}
                                />
                            </div>


                            <div className="formField2">

                                <button className="formFieldButton"> Sign Up</button>



                                <NavLink to="/sign-in" className="formFieldLink">
                                    I am already a member
                                </NavLink>
                            </div>

                        </form>
                    </div>
                </div>

            </div>

        )
    }
}

export default SignUpForm;