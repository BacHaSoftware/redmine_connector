
<a name="readme-top"></a>

<!-- PROJECT DETAILS -->
<br />
<div align="center">
  <a href="https://github.com/BacHaSoftware/redmine_connetor">
    <img src="/bhs_connector_redmine/static/description/icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Redmine Integration</h3>

  <p align="center">
    A product of Bac Ha Software allows synchronized log work from Redmine to Odoo, notify via Slack about missing log work.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact-us">Contact us</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<div align="left">
  <a href="https://github.com/BacHaSoftware/redmine_connetor">
    <img src="/bhs_connector_redmine/static/description/imgs/screen/setting.png" alt="Setting">
  </a>
<div align="center">Connect To Redmine</div> 
</div>

<div align="left">
  <a href="https://github.com/BacHaSoftware/redmine_connetor">
    <img src="/bhs_connector_redmine/static/description/imgs/screen/cron.png" alt="Setting">
  </a>
<div align="center">Synchronize Log Work</div> 
</div>

<div align="left">
  <a href="https://github.com/BacHaSoftware/redmine_connetor">
    <img src="/bhs_connector_redmine/static/description/imgs/screen/timesheet.png" alt="Setting">
  </a>
<div align="center">Record Log Work Data</div> 
</div>

#### Key Features:

🌟 <code>Connect To Redmine</code>: nstall library python-redmine, install this module on Odoo. Then input Redmine page and Redmine API Key in General Settings.

🌟 <code>Synchronize Log Work</code>: Data from redmine is synchronized to Odoo by schedule action at the end of the day and weekend to ensure consistency.

🌟 <code>Record Log Work Data</code>: Log work data will be recorded in 0000-Redmine project and display on Timesheet. Now you can manage easily and effectively working time of your employees.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

<!-- PREREQUISTES  -->
### Prerequisites

This module needs the Python library <code>python-redmine</code>, otherwise it cannot be installed and used. Install it through the command
  ```sh
  sudo pip3 install python-redmine
  ```

### Installation

1. Install module  <code>bhs_connector_redmine</code>
2. Config parameter page and api key connect in Setting Odoo

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

You want to synchronize working time data from Redmine to Odoo for easy management, and you want to automatically notify users when they forget their logwork, then this is a great solution for you.

#### Featured Highlight:

🌟 <code>Automatic Synchronize</code>: Synchronize automatically daily and weekly log work data from redmine to Odoo, record it in 0000-Redmine project.

🌟 <code>Notify Via Slack</code>: Slack notifications for staffs who haven't logged enough time. Send notification to Slack users and channel.

🌟 <code>Simple Setup</code>: Adjust settings directly from the General Settings menu, easy connect to your organization's redmine.

🌟 <code>Display On Timesheet</code>: Log work data will be displayed on Odoo Timesheet, managing employee working time will be more convenient.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT US-->
## Contact us
Need assistance with setup or have any concerns? Contact Bac Ha Software directly for prompt and dedicated support:
<div align="left">
  <a href="https://github.com/BacHaSoftware">
    <img src="/bhs_connector_redmine/static/description/imgs/logo.png" alt="Logo" height="80">
  </a>
</div>

📨 odoo@bachasoftware.com

🌍 [https://bachasoftware.com](https://bachasoftware.com)

[![WEBSITE][website-shield]][website-url] [![LinkedIn][linkedin-shield]][linkedin-url]

Project Link: [https://github.com/BacHaSoftware/redmine_connetor](https://github.com/BacHaSoftware/redmine_connetor)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-url]: https://github.com/BacHaSoftware/redmine_connetor/blob/17.0/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/bac-ha-software
[website-shield]: https://img.shields.io/badge/-website-black.svg?style=for-the-badge&logo=website&colorB=555
[website-url]: https://bachasoftware.com