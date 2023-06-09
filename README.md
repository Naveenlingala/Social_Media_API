# Social Media API

The API provides a variety of functionalities including fetching user profiles, following other users, uploading posts, deleting posts, liking posts, unliking previously liked posts, and commenting on posts.

## Running the Web App using Docker
This repository contains a Dockerfile that can be used to build and run the web app using Docker. Follow the instructions below to build and run the Docker container.

### Prerequisites
Before you can build and run the Docker container, you must have Docker installed on your system. If you do not already have Docker installed, follow the installation instructions for your platform from the [Docker documentation](https://docs.docker.com/get-docker/).

### Building the Docker Image
To build the Docker image, navigate to the root directory of the project where the Dockerfile is located and run the following command:

```
docker build -t web-app .
```

This command will build the Docker image and tag it with the name web-app.

### Running the Docker Container
To run the Docker container, use the following command:

```
docker run -p 8000:8000 web-app
```

This command will start the container and map port 8000 of the container to port 8000 of your host machine. You can now access the web app by navigating to http://localhost:8000 in your web browser.


## API Endpoints
> **_NOTE:_**: The Hosted Link can be tested using **Postman** 
### Account details
- Naveen(username: naveen, password: 123456789)


![image](https://user-images.githubusercontent.com/60232407/226263689-88def42a-8b9a-4a26-9802-04c75b2380a1.png)

- Add jwt token to Authorization for each request

![image](https://user-images.githubusercontent.com/60232407/226264070-1151b6fb-cfad-4b14-a6b4-cfa5f3920ce8.png)

- Input values should added to the body(form-data) Example:-

![image](https://user-images.githubusercontent.com/60232407/226264936-bb9f9e4e-392e-4162-8673-730b74bf7d80.png)


### User Authentication
- POST [/api/authenticate](https://social-media-api-tm6v.onrender.com/api/authenticate)
  - INPUT: Username, Password
  - RETURN: JWT token

### Follow a user
- POST [/api/follow/{id}](https://social-media-api-tm6v.onrender.com/api/follow/0)
    - Authenticated user would follow user with {id}

### Unfollow a User
- POST [/api/unfollow/{id}](https://social-media-api-tm6v.onrender.com/api/unfollow/0) 
    - Authenticated user would unfollow a user with {id}
      
### Get User Profile
- GET [/api/user](https://social-media-api-tm6v.onrender.com/api/user) 
    - Authenticates the request and return the respective user profile.
    - RETURN: User Name, number of followers & followings.
 
### Add New Post
- POST [api/posts/](https://social-media-api-tm6v.onrender.com/api/posts/) 
    - Adds a new post created by the authenticated user.
    - Input: Title, Description
    - RETURN: Post-ID, Title, Description, Created Time(UTC).
    
### Delete a Post
- DELETE [api/posts/{id}](https://social-media-api-tm6v.onrender.com/api/posts/0) 
    - Deletes post with {id} created by the authenticated user.
      
### Like a Post
- POST [/api/like/{id}](https://social-media-api-tm6v.onrender.com/api/like/0) 
    - Likes the post with {id} by the authenticated user.
  
### Unlike a Post
- POST [/api/unlike/{id}](https://social-media-api-tm6v.onrender.com/api/unlike/0) 
    - Unlikes the post with {id} by the authenticated user.
      
### Add Comment to a Post
- POST [/api/comment/{id}](https://social-media-api-tm6v.onrender.com/api/comment/0) 
    - Adds a comment for post with {id} by the authenticated user.
    - Input: Comment
    - Return: Comment-ID
  
### Get Single Post with Likes and Comments
- GET [api/posts/{id}](https://social-media-api-tm6v.onrender.com/api/posts/1) 
    - Returns a single post with {id} populated with its number of likes and comments
   
### Get All Posts by Authenticated User
 - GET [/api/all_posts](https://social-media-api-tm6v.onrender.com/api/all_posts) 
    - would return all posts created by authenticated user sorted by post time.
    - RETURN: For each post return the following values
      - id: ID of the post 
      - title: Title of the post 
      - desc: Description of the post 
      - created_at: Date and time when the post was created 
      - comments: Array of comments, for the particular post
      - likes: Number of likes for the particular post
