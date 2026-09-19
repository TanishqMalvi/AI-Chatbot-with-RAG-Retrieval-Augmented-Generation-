"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { authApi } from "../../lib/api";
import { clsx } from "clsx";

type FormErrors = Record<string, string>;

export const AuthForm = ({ onLogin }: { onLogin: () => void }) => {
  const [formType, setFormType] = useState<"login" | "signup">("login");
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const toggleForm = () => setFormType((current) => current === "login" ? "signup" : "login");

  useEffect(() => {
    if (!isLoading) {
      setErrors({});
    }
  }, [isLoading]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (isLoading) return;

    try {
      const formData = new FormData(event.currentTarget);
      const data = Object.fromEntries(formData);
      const getValue = (key: string) => {
        const value = data[key];
        return typeof value === "string" ? value : "";
      };
      const email = getValue("email").trim();
      const password = getValue("password");

      if (formType === "login") {
        await authApi.login(email, password);
      } else {
        const confirmPassword = getValue("confirmPassword");
        if (password !== confirmPassword) {
          setErrors({ form: "Passwords do not match." });
          return;
        }
        await authApi.signup(email, password);
      }
      onLogin();
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Login failed.";
      setErrors({ form: message });
    }
  };

  return (
    <div className={clsx(
      "w-full max-w-md fixed inset-0 mx-auto flex flex-col items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4 rounded-xl",
      "overflow-hidden"
    )}>
      <div className="w-full bg-white/5 rounded-xl p-6 shadow-lg transition-all duration-300">
        <div className="text-center mb-6">
          <div className="flex gap-2">
            {formType === "login" && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
              >
                <div style={{ width: 40, height: 40, background: "linear-gradient(135deg,#6366F1,#8B5CF6)", borderRadius: 12 }} />
              </motion.div>
            )}
            {formType === "signup" && (
              <div style={{ width: 32, height: 32, borderRadius: 10, background: "linear-gradient(135deg,#00D4FF,#7C3AED)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                👤
              </div>
            )}
          </div>
          <h2 className="mb-2 text-2xl font-bold text-slate-900">HealthTech RAG Assistant</h2>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
          <div className="flex flex-col">
            <div className="flex flex-col">
              <label className="mb-1 text-xs font-medium text-slate-600 leading-none">
                {formType === "login" ? "User ID" : "Full Name"}
              </label>
              <motion.input
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                name={formType === "login" ? "userId" : "fullName"}
                type="text"
                className="flex-1 px-3 py-2.5 border border-slate-700/50 rounded-xl bg-slate-950/50 focus:ring-2 focus:ring-cyan-400/50 text-sm text-slate-100 transition-all duration-200"
                placeholder={formType === "login" ? "Enter user ID" : "John Doe"}
              />
            </div>

            {!formType.includes("login") ? (
              <div className="flex justify-between items-center">
                <p className="text-xs text-slate-500">{formType === "login" ? "Don't have an account?" : "Already have an account?"}</p>
              </div>
            ) : (
              <>
                {errors.userId && <p className="text-sm text-red-400 text-right">{errors.userId}</p>}
              </>
            )}
          </div>

          <div className="input-group">
            <label className="mb-2 text-sm font-medium text-white">
              {formType === "login" ? "Role" : "Account Type"}
            </label>
            <motion.div className="flex gap-2 justify-center mt-1">
              <motion.button
                type="button"
                key="doctor"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={clsx(
                  "px-4 py-2 rounded-xl text-sm font-medium italic bg-slate-950/40 border border-slate-700/50 text-slate-300 transition-all",
                  "hover:bg-slate-950/60"
                )}
                onClick={() => setFormType("login")}
              >
                Doctor
              </motion.button>
              <motion.button
                type="button"
                key="patient"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={clsx(
                  "px-4 py-2 rounded-xl text-sm font-medium italic bg-slate-950/40 border border-slate-700/50 text-slate-300 transition-all",
                  "hover:bg-slate-950/60"
                )}
                onClick={() => setFormType("signup")}
              >
                Patient
              </motion.button>
            </motion.div>
          </div>

          {errors.form && (
            <p className="text-sm text-red-400 italic text-right">{errors.form}</p>
          )}

          <div style={{ textAlign: "right" }}>
            {isLoading ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                🔁 Loading...
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                {formType === "login" ? "Sign In" : "Create Account"}
              </motion.div>
            )}
          </div>
        </form>

        {!formType.includes("login") && (
          <div className="mt-4 flex justify-between items-center text-sm text-slate-500">
            <button
              type="button"
              onClick={() => router.push("/")}
              className="px-2 py-1 rounded-md bg-transparent hover:bg-opacity-10 transition-colors"
            >
              ← Back to Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
