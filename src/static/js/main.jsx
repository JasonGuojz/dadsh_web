// import { Button } from 'reactstrap';
// import React from 'react';
const Button = window.Reactstrap.Button;

const Collapse = window.Reactstrap.Collapse;
const Navbar = window.Reactstrap.Navbar;
const NavbarBrand = window.Reactstrap.NavbarBrand;
const Nav = window.Reactstrap.Nav;
const NavItem = window.Reactstrap.NavItem;
const NavLink = window.Reactstrap.NavLink;


const Router = window.ReactRouterDOM.BrowserRouter;
const Route = window.ReactRouterDOM.Route;
const ReactMarkdown = window.ReactMarkdown;

const Form = window.Reactstrap.Form;
const FormGroup = window.Reactstrap.FormGroup;
const Label = window.Reactstrap.Label;
const Input = window.Reactstrap.Input;


const UncontrolledDropdown = window.Reactstrap.UncontrolledDropdown;
const Dropdown = window.Reactstrap.Dropdown;
const DropdownToggle = window.Reactstrap.DropdownToggle;
const DropdownMenu = window.Reactstrap.DropdownMenu;
const DropdownItem = window.Reactstrap.DropdownItem;
const Spinner = window.Reactstrap.Spinner;


const axios = window.axios;

const Select = window.Select;

const head = "https://dadsh-cifar10.oss-cn-shenzhen.aliyuncs.com";


class About extends React.Component {
    //

// Use the render function to return JSX component
    render() {
        return (

            <div>
                <h1>About</h1>
                <ReactMarkdown source={window.APP_CONFIG.about}/>
            </div>
        );
    }
}


// Create a ES6 class component
class MainPage extends React.Component {
    //

    constructor(props) {
        super(props);
        this.state = {
            file: null,
            predictions: [],
            imageSelected: false,
            url: null,
            isLoading: false,
            selectedOption: null,
            predictionsurl: [],
            ispredicted: false,

        }
    }

    _onFileUpload = (event) => {
        this.setState({
            rawFile: event.target.files[0],
            file: URL.createObjectURL(event.target.files[0]),
            imageSelected: true
        })
    };

    _onUrlChange = (url) => {
        this.state.url = url;
        if ((url.length > 5) && (url.indexOf("http") === 0)) {
            this.setState({
                file: url,
                imageSelected: true
            })
        }
    };

    _clear = async (event) => {
        this.setState({
            file: null,
            imageSelected: false,
            predictions: [],
            rawFile: null,
            url: ""
        })
    };

    _predict = async (event) => {
        this.setState({isLoading: true});

        let resPromise = null;
        if (this.state.rawFile) {
            const data = new FormData();
            data.append('file', this.state.rawFile);
            resPromise = axios.post('/predict', data);
        } else {
            resPromise = axios.get('/predict', {
                params: {
                    url: this.state.file
                }
            });
        }

        try {
            const res = await resPromise;
            const payload = res.data;

            this.setState({predictions: payload.predictions, isLoading: false});
            console.log(payload)
        } catch (e) {
            alert(e)
        }
    };


    renderPrediction() {
        const predictions = this.state.predictions || [];

        if (predictions.length > 0) {

            // for (var i = 0; i < predictions.length; i++) {
            //     var columns = [];
            //     var imgURL;
            //     for (var j = 0; j < projectImgs.length; j++) {
            //         if (projectImgs[j].indexOf(predictions[i].img) > 0) {
            //
            //         }
            //     }
            // }
            return (
                <div className="pics6">
                    <div id="status1_pics">
                        <ul className="list_result1">
                            <li>
                                <img src={head + predictions[0]} className={"result1"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[0]}</div>
                            </li>
                            <li>
                                <img src={head + predictions[1]} className={"result2"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[1]}</div>
                            </li>
                            <li>
                                <img src={head + predictions[2]} className={"result3"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[2]}</div>
                            </li>
                            <li>
                                <img src={head + predictions[3]} className={"result4"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[3]}</div>
                            </li>
                        </ul>
                    </div>
                    <div id="status2_pics">
                        <ul className="list_result2">
                            <li>
                                <img src={head + predictions[4]} className={"result5"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[4]}</div>
                            </li>
                            <li>
                                <img src={head + predictions[5]} className={"result6"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[5]}</div>
                            </li>
                            <li>
                                <img src={head + predictions[6]} className={"result7"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[6]}</div>
                            </li>
                            <li>
                                <img src={head + predictions[7]} className={"result8"} hidden={!this.state.imageSelected}/>
                                <div>{predictions[6]}</div>
                            </li>
                        </ul>
                    </div>
                </div>



            )

        } else {
            return null
        }
    }

    handleChange = (selectedOption) => {
        this.setState({selectedOption});
        console.log(`Option selected:`, selectedOption);
    };

    sampleUrlSelected = (item) => {
        this._onUrlChange(item.url);
    };

    render() {
        const sampleImages = APP_CONFIG.sampleImages;
        return (
            <div>
                <h2>{APP_CONFIG.description}</h2>
                <Form>
                    <br />
                    <h4>Provide a URL</h4>
                    <FormGroup>
                        <div>
                            <div>

                                <UncontrolledDropdown>
                                    <DropdownToggle caret>
                                        Sample Image List
                                    </DropdownToggle>
                                    <DropdownMenu>
                                        {sampleImages.map(si =>
                                            <DropdownItem onClick={() => this.sampleUrlSelected(si)}>
                                                {si.name}
                                            </DropdownItem>)
                                        }

                                    </DropdownMenu>
                                </UncontrolledDropdown>

                            </div>
                            <Input value={this.state.url} name="file"
                                   onChange={(e) => this._onUrlChange(e.target.value)}
                                   placeholder="or provide a URL"
                            />

                        </div>
                    </FormGroup>
                    <br />
                    <h4>Upload an image</h4>
                    <FormGroup id={"upload_button"}>
                        <Label for="imageUpload">
                            <Input type="file" name="file" id="imageUpload" accept=".png, .jpg, .jpeg" ref="file"
                                   onChange={this._onFileUpload}/>
                            <span className="btn btn-primary">Upload</span>
                        </Label>
                    </FormGroup>

                    <img src={this.state.file} className={"img-preview"} hidden={!this.state.imageSelected}/>

                    <br />
                    <FormGroup>
                        <Button outline color="success" onClick={this._predict}
                                disabled={this.state.isLoading}> Predict</Button>
                        <span className="p-1 "/>
                        <Button outline color="danger" onClick={this._clear}> Clear</Button>
                    </FormGroup>


                    {this.state.isLoading && (
                        <div>
                            <Spinner color="primary" type="border" style={{width: '5rem', height: '5rem'}}/>

                        </div>
                    )}

                </Form>

                {this.renderPrediction()}


            </div>
        );
    }
}

class CustomNavBar extends React.Component {


    render() {
        const link = APP_CONFIG.code;
        return (
            <Navbar color="light" light fixed expand="md">
                <NavbarBrand href="/">{APP_CONFIG.title}</NavbarBrand>
                <Collapse navbar>
                    <Nav className="ml-auto" navbar>
                        <NavItem>
                            <NavLink href="/about">About</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href={link}>GitHub</NavLink>
                        </NavItem>

                    </Nav>
                </Collapse>
            </Navbar>
        )
    }
}

// Create a function to wrap up your component
function App() {


    return (
        <Router>
            <div className="App">
                <CustomNavBar/>
                <div>
                    <main role="main" className="container">
                        <Route exact path="/" component={MainPage}/>
                        <Route exact path="/about" component={About}/>

                    </main>
                </div>
            </div>
        </Router>
    )
}

(async () => {
    const response = await fetch('/config');
    const body = await response.json();

    window.APP_CONFIG = body;

    // Use the ReactDOM.render to show your component on the browser
    ReactDOM.render(

        <App />,
        document.getElementById('container')
    )
})();
