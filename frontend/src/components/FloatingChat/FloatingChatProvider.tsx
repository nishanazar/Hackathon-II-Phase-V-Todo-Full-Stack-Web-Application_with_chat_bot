'use client';

import { ReactNode } from 'react';
import FloatingChatWidget from './FloatingChatWidget';

type Props = {
  children: ReactNode;
};

const FloatingChatProvider = ({ children }: Props) => {
  return (
    <>
      {children}
      <FloatingChatWidget />
    </>
  );
};

export default FloatingChatProvider;