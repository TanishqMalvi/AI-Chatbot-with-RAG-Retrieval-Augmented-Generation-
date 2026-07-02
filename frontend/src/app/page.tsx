"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authApi } from "../lib/api";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (authApi.isAuthenticated()) {
      router.replace("/chat");
    } else {
      router.replace("/login");
    }
  }, []);

  return null; // blank while redirecting
}