export function getToken() {
  return localStorage.getItem("token");
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

export function decodeToken() {
  const token = getToken();
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload;
  } catch {
    return null;
  }
}

export function isAuthenticated() {
  const payload = decodeToken();
  if (!payload) return false;

  // check expiration
  if (payload.exp * 1000 < Date.now()) {
    logout();
    return false;
  }

  return true;
}

export function isAdmin() {
  const payload = decodeToken();
  return payload?.is_admin === true;
}
