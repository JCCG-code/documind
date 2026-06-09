/**
 * Allows to check item type
 * @param item - item received to check type
 * @returns True if item is Document
 */
export const isDocument = (item: unknown): item is Document => {
  // Cast to see item components
  const obj = item as Record<string, unknown>
  // Return statement
  return (
    typeof item === 'object' &&
    item !== null &&
    typeof obj.content_type === 'string' &&
    typeof obj.filename === 'string' &&
    typeof obj.hash === 'string' &&
    typeof obj.size === 'number'
  )
}

/**
 * Allows to check array of documents
 * @param arr - array received
 * @returns True if arr is Document[]
 */
export const isArrayDocument = (arr: unknown): arr is Document[] => {
  // Return statement
  return Array.isArray(arr) && arr.every(isDocument)
}
