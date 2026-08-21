export async function apiRequest<T>(
  url: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    if (typeof data?.detail === 'string') {
      throw new Error(data.detail);
    }

    if (Array.isArray(data?.detail)) {
      const message = data.detail
        .map((item: any) => {
          const field = item.loc?.at(-1) ?? 'field';
          return `${field}: ${item.msg}`;
        })
        .join('; ');

      throw new Error(message);
    }

    throw new Error(
      `Request failed with status ${response.status}`,
    );
  }

  return data as T;
}
