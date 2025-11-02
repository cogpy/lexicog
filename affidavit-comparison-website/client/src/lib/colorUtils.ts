/**
 * Get color for AD paragraph based on severity (1-10)
 * 1-3: Green (neutral)
 * 4-6: Yellow/Orange (moderate)
 * 7-10: Red (serious allegation)
 */
export function getSeverityColor(severity: number = 5): string {
  if (severity <= 3) {
    return "bg-green-50 border-green-200 dark:bg-green-950/30 dark:border-green-800";
  } else if (severity <= 6) {
    return "bg-yellow-50 border-yellow-200 dark:bg-yellow-950/30 dark:border-yellow-800";
  } else {
    return "bg-red-50 border-red-200 dark:bg-red-950/30 dark:border-red-800";
  }
}

/**
 * Get badge color for AD paragraph based on severity
 */
export function getSeverityBadgeColor(severity: number = 5): string {
  if (severity <= 3) {
    return "bg-green-600 hover:bg-green-700";
  } else if (severity <= 6) {
    return "bg-yellow-600 hover:bg-yellow-700";
  } else {
    return "bg-red-600 hover:bg-red-700";
  }
}

/**
 * Get color for response based on evidence strength (1-10)
 * Higher values = stronger evidence = deeper blue
 */
export function getEvidenceColor(strength: number = 5): string {
  if (strength <= 3) {
    return "bg-blue-50 border-blue-100 dark:bg-blue-950/20 dark:border-blue-900";
  } else if (strength <= 6) {
    return "bg-blue-100 border-blue-200 dark:bg-blue-950/40 dark:border-blue-800";
  } else {
    return "bg-blue-200 border-blue-300 dark:bg-blue-950/60 dark:border-blue-700";
  }
}

/**
 * Get badge color for response based on evidence strength
 */
export function getEvidenceBadgeColor(strength: number = 5): string {
  if (strength <= 3) {
    return "bg-blue-400 hover:bg-blue-500";
  } else if (strength <= 6) {
    return "bg-blue-600 hover:bg-blue-700";
  } else {
    return "bg-blue-800 hover:bg-blue-900";
  }
}

/**
 * Parse annexures from JSON string
 */
export function parseAnnexures(annexuresJson: string | null): string[] {
  if (!annexuresJson) return [];
  try {
    return JSON.parse(annexuresJson);
  } catch {
    return [];
  }
}
