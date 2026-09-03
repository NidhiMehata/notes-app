import API_BASE_URL from "./client";

export async function login(email: string, password: string) {
  const body = new URLSearchParams();

  body.append("username", email);
  body.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  const data = await response.json();

  if (!response.ok) {
    if (response.status >= 500) {
      throw new Error("Something went wrong. Please try again.");
    }

    throw new Error(data.detail ?? "Failed to login");
  }

  return data;
}