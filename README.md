
<h3 align="center">Stitch Pattern Generator</h3>

  <p align="center">
    Convert a sentence into a stitching pattern in a variety of fonts and sizes
    <br />
  </p>




<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT-->
## About

Created by: Zachary Sherman  
Github: zcsherm  
Class: CS361 - Summer 2025  
Target Team Member: Anna Marine

This is a small microservice that uses ZeroMQ to communicate. It can be passed a phrase, a desired font, and a font size. It will then convert this message into a matrix that represents a knitting pattern.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This microservice must be run locally on your machine. There are several dependencies you must install prior to running the application:  
* PIL - A python Library for image editing
* ZeroMQ - A python library for server communication
* FontTools - A python library for parsing .TTF files
### Prerequisites

* Windows 10 and above. Support for Linux and Mac coming soon.

* PIL
  ```sh
  pip install Pillow
  ```
* ZeroMQ
  ```sh
  pip install pyzmq
  ```

* FontTools
    ```commandline
    pip install fonttools
    ```
### Installation

1. Download the source or clone the repo
2. Install the prerequisites above
3. Update your path your Windows/Fonts folder and the default socket if desired
4. Launch main.py as a standalone or from your IDE

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Calling
Using this microservice requires communicating over a socket. Requests must be an object in the form of:

    {
     "type":type_of_request,
     "message":message_to_convert,
     "font":font_name,
     "size":font_size,
     "max_size" maximum_length
    }
* Type:  
  * "convert" : Converts the passed message into a matrix

* Message:
  * string : The message to be converted. (Some fonts do not support all characters)

* Font:
  * string : The desired font name. 'basic' will pick the simplest font, the best fit from the windows fonts will be determined for other entries
    * 'Basic' - A simple and effective font for knitting patterns
    * Any other string - The closest matching font built in to windows will be selected. (Note: some fonts are not tested and can be volatile, such as wingdings)

* Size:
  * int or string: The desired font size.
    * int - Roughly correlates to the height in pixels of built in fonts
    * string - 'small', 'medium', or 'large'. 
      * These correspond to the defaults configured in the .ini file
      * These must be used when choosing the basic font. Each scales up the basic font.

* Max size:
  * int - The maximum length that the returned phrase can be.
    * If the matrix is longer than this max size, then the microservice will return an error instead
  * None - Set to None to not worry about size limits
  
### Returning data

The microservice will send an object back of the following structure:

    {
    "type" : return_type
    "message" : return_details
    }

* Type:
  * string: 
    * 'matrix' if the conversion was successful
    * 'error' if the conversion failed

* Message:
  * string or a 2d list:
    * string - If an error was sent, this will contain the error message
    * list - 2d matrix if the conversion succeeded
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Examples:
#### Input:
    # Build the message
    data = {'type':'convert',
            'message':'hello',
            'font':'basic',
            'size':'small',
            'max_size':None}

    # Send the request
    socket.send_json(data)

    # Get the reply
    conversion = socket.recv_json()
    
    # Check if the reply was resulted in an error
    if conversion['type'] == 'error':
        print(f"Conversion Failed with message: {conversion['message']}")

    # display the received matrix
    else:
        for row in conversion['message']:
            print(row)

#### Output

    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
    [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0]
![img.png](example1.png)
<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/github_username/repo_name/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
