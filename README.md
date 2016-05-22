# Touch-Login

## Contacting the API from a third-party site

* **URL**

  https://alpha-006-dot-touch-login.appspot.com/_ah/api/touchloginAPI/v1/AuthenticateUser

* **Method**

  `POST`

* **URL Parameters**

  **Required**
  	`origin = [String]`
    `username=[String]`

* **Success Response**

  * **Code:** 200 <br />

* **Error Response**
  * **Code:** 400 <br />
    **Content:** `{ error: "Authentication not found" }`

  * **Code:** 401 <br />
    **Content:** `{ error: "User did not request authentication" }`

  * **Code:** 408 <br />
    **Content:** `{ error: "Authentication request timeout" }`

  * **Code:** 422 <br />
    **Content:** `{ error: "User not found" }`