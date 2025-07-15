

export const fetchData = async (url: string): Promise<string> => {

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
  }

  return await response.text();
};