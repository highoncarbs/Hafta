export default async function ({ $auth, redirect, store }) {
    let user = $auth.loggedIn;
    if (user) {

    }
    else {
        redirect('/auth')
    }
}