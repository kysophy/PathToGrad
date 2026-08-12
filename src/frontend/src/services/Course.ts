export type OpeningClass = {
  section: string;
  instructor: string;
  enrolled: number;
  capacity: number;
};

export type Course = {
  id: string;
  name: string;
  credits: number;
  prerequisiteChain: string[];
  status: string;
  color: 'yellow' | 'pink';
  openingClasses: OpeningClass[];
  note?: string;
};